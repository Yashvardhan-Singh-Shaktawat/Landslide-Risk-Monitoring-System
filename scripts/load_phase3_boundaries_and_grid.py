"""
Phase 3 Loader: Load data_sources, 8 NER state outlines, DataMeet 2011 districts,
and the Pan-NER 5 km grid (~10.5k cells) into Supabase PostGIS.
Also runs spatial verification queries (ST_Contains, ST_DWithin) and reports DB size.
"""

import os
import sys
import json
import math
from datetime import date
from dotenv import load_dotenv
import psycopg
import shapefile
from shapely.geometry import shape, Polygon, MultiPolygon, box
from shapely.ops import transform

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(PROJECT_ROOT, "backend", ".env")
STATE_GEOJSON = os.path.join(PROJECT_ROOT, "ml", "data", "raw", "boundaries", "india_state.geojson")
DATAMEET_SHP = os.path.join(PROJECT_ROOT, "ml", "data", "raw", "boundaries", "datameet_2011", "2011_Dist.shp")

NER_8_STATES = {
    "Arunachal Pradesh", "Assam", "Manipur", "Meghalaya",
    "Mizoram", "Nagaland", "Sikkim", "Tripura"
}

STATE_NAME_NORMALIZE = {
    "Arunanchal Pradesh": "Arunachal Pradesh",
}

STATE_CODES = {
    "Arunachal Pradesh": "AR",
    "Assam": "AS",
    "Manipur": "MN",
    "Meghalaya": "ML",
    "Mizoram": "MZ",
    "Nagaland": "NL",
    "Sikkim": "SK",
    "Tripura": "TR",
}


def normalize_psycopg_url(url: str) -> str:
    if url.startswith("postgresql+psycopg://"):
        return "postgresql://" + url[len("postgresql+psycopg://"):]
    if url.startswith("postgresql+psycopg2://"):
        return "postgresql://" + url[len("postgresql+psycopg2://"):]
    return url


def ensure_multipolygon(geom):
    if isinstance(geom, Polygon):
        return MultiPolygon([geom])
    return geom


def main():
    load_dotenv(ENV_PATH)
    raw_url = os.getenv("DATABASE_URL", "").strip()
    if not raw_url:
        print("ERROR: DATABASE_URL is not set in backend/.env.")
        sys.exit(1)

    conn_url = normalize_psycopg_url(raw_url)

    with psycopg.connect(conn_url) as conn:
        with conn.cursor() as cur:
            # 1. Insert data_sources with licence & access_date
            sources = [
                (
                    "NASA Global Landslide Catalog (GLC) / COOLR",
                    "https://data.nasa.gov/earth-science/Global-Landslide-Catalog-Export/dd9e-wu2v",
                    "CC0 1.0 Universal (Public Domain)",
                    date(2026, 11, 23),
                    "Global (359 cleaned NER GLC + 98 COOLR open submissions)",
                    "Point coordinates with location_accuracy (1km-100km)",
                    "Road/urban reporting bias (81.9% text mention); coarse accuracy >=10km for 53.2% of NER events.",
                ),
                (
                    "DataMeet India Maps (Census 2011 Districts)",
                    "https://github.com/datameet/maps/tree/master/Districts/Census_2011",
                    "MIT License (Copyright (c) 2020 DataMeet India community)",
                    date(2026, 11, 25),
                    "Pan-India (2011 districts: Manipur 9, Sikkim 4; since reorganised)",
                    "Polygon boundaries (10.29 MB shapefile package)",
                    "Not official Survey of India; predates Manipur 2016 (16) and Sikkim 2021 (6) reorganisations.",
                ),
                (
                    "NER State Outlines (Open GeoJSON Derivative)",
                    "ml/data/raw/boundaries/india_state.geojson",
                    "GADM-style non-commercial academic derivative (upstream version unverified)",
                    date(2026, 11, 23),
                    "8 North Eastern States of India",
                    "Polygon boundaries",
                    "Educational approximation only; not official Survey of India demarcation.",
                ),
            ]
            for s in sources:
                cur.execute(
                    """
                    INSERT INTO public.data_sources (name, url, licence, access_date, coverage, resolution, limitations)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (name) DO UPDATE SET
                        url = EXCLUDED.url,
                        licence = EXCLUDED.licence,
                        access_date = EXCLUDED.access_date,
                        coverage = EXCLUDED.coverage,
                        resolution = EXCLUDED.resolution,
                        limitations = EXCLUDED.limitations;
                    """,
                    s,
                )
            conn.commit()
            print("Loaded data_sources.")

            # 2. Load 8 NER States
            with open(STATE_GEOJSON, "r", encoding="utf-8") as f:
                st_data = json.load(f)

            state_geoms = {}
            state_id_map = {}
            for feat in st_data["features"]:
                name = feat["properties"].get("NAME_1", "").strip()
                if name not in NER_8_STATES:
                    continue
                geom = ensure_multipolygon(shape(feat["geometry"]))
                state_geoms[name] = geom
                cur.execute(
                    """
                    INSERT INTO public.states (name, code, boundary_source, geom)
                    VALUES (%s, %s, %s, extensions.ST_GeomFromText(%s, 4326))
                    ON CONFLICT (name) DO UPDATE SET
                        code = EXCLUDED.code,
                        geom = EXCLUDED.geom
                    RETURNING id;
                    """,
                    (name, STATE_CODES.get(name), "india_state.geojson (educational approximation)", geom.wkt),
                )
                state_id_map[name] = cur.fetchone()[0]
            conn.commit()
            print(f"Loaded {len(state_id_map)} NER states.")

            # 3. Load DataMeet 2011 Districts for NER
            sf = shapefile.Reader(DATAMEET_SHP)
            dist_count = 0
            for sr in sf.shapeRecords():
                rec = sr.record.as_dict()
                raw_st = str(rec.get("ST_NM", "")).strip()
                st_name = STATE_NAME_NORMALIZE.get(raw_st, raw_st)
                dist_name = str(rec.get("DISTRICT", "")).strip()
                if st_name not in NER_8_STATES:
                    continue
                geom = ensure_multipolygon(shape(sr.shape.__geo_interface__))
                cur.execute(
                    """
                    INSERT INTO public.districts (state_id, state_name, name, vintage_label, geom)
                    VALUES (%s, %s, %s, %s, extensions.ST_GeomFromText(%s, 4326))
                    ON CONFLICT (state_name, name) DO UPDATE SET
                        geom = EXCLUDED.geom,
                        vintage_label = EXCLUDED.vintage_label;
                    """,
                    (
                        state_id_map.get(st_name),
                        st_name,
                        dist_name,
                        "2011 districts (Manipur 9, Sikkim 4; since reorganised)",
                        geom.wkt,
                    ),
                )
                dist_count += 1
            conn.commit()
            print(f"Loaded {dist_count} DataMeet 2011 NER districts.")

            # 4. Generate & Load 5 km Grid Cells for NER Mask Only (~10.5k cells)
            # Local metric projection centered at (92.5E, 26.0N), matching Option E
            R = 6371.0
            lat0, lon0 = 26.0, 92.5
            cos_lat0 = math.cos(math.radians(lat0))

            def to_km(lon, lat):
                return (
                    (lon - lon0) * math.radians(1) * R * cos_lat0,
                    (lat - lat0) * math.radians(1) * R,
                )

            def to_lonlat(x_km, y_km):
                return (
                    lon0 + x_km / (math.radians(1) * R * cos_lat0),
                    lat0 + y_km / (math.radians(1) * R),
                )

            # Union NER states to check intersection
            from shapely.ops import unary_union
            ner_union = unary_union(list(state_geoms.values()))
            minx, miny, maxx, maxy = ner_union.bounds
            x_min_km, y_min_km = to_km(minx, miny)
            x_max_km, y_max_km = to_km(maxx, maxy)

            cx_start = math.floor(x_min_km / 5.0)
            cx_end = math.ceil(x_max_km / 5.0)
            cy_start = math.floor(y_min_km / 5.0)
            cy_end = math.ceil(y_max_km / 5.0)

            grid_rows = []
            for cx in range(cx_start, cx_end + 1):
                for cy in range(cy_start, cy_end + 1):
                    x0, y0 = cx * 5.0, cy * 5.0
                    x1, y1 = x0 + 5.0, y0 + 5.0
                    lon_w, lat_s = to_lonlat(x0, y0)
                    lon_e, lat_n = to_lonlat(x1, y1)
                    cell_poly = box(lon_w, lat_s, lon_e, lat_n)
                    if not ner_union.intersects(cell_poly):
                        continue
                    c_pt = cell_poly.centroid
                    assigned_st = None
                    for st_name, st_geom in state_geoms.items():
                        if st_geom.contains(c_pt):
                            assigned_st = state_id_map[st_name]
                            break
                    if assigned_st is None:
                        # Fallback to first intersecting state
                        for st_name, st_geom in state_geoms.items():
                            if st_geom.intersects(cell_poly):
                                assigned_st = state_id_map[st_name]
                                break
                    cell_code = f"NER5K_{cx}_{cy}"
                    grid_rows.append((cell_code, 5.0, assigned_st, True, c_pt.y, c_pt.x, cell_poly.wkt))

            cur.executemany(
                """
                INSERT INTO public.grid_cells (cell_code, grid_size_km, state_id, in_study_area, centroid_lat, centroid_lon, geom)
                VALUES (%s, %s, %s, %s, %s, %s, extensions.ST_GeomFromText(%s, 4326))
                ON CONFLICT (cell_code) DO NOTHING;
                """,
                grid_rows,
            )
            conn.commit()
            print(f"Loaded {len(grid_rows)} 5 km NER grid cells.")

            # 5. Spatial verification queries (test point: Gangtok 27.3389N, 88.6065E)
            cur.execute(
                """
                SELECT s.name, d.name
                FROM public.states s
                JOIN public.districts d ON d.state_id = s.id
                WHERE extensions.ST_Contains(d.geom, extensions.ST_SetSRID(extensions.ST_MakePoint(88.6065, 27.3389), 4326));
                """
            )
            print("ST_Contains test (Gangtok 27.3389N, 88.6065E):", cur.fetchone())

            cur.execute(
                """
                SELECT COUNT(*)
                FROM public.grid_cells
                WHERE extensions.ST_DWithin(
                    geom::extensions.geography,
                    extensions.ST_SetSRID(extensions.ST_MakePoint(88.6065, 27.3389), 4326)::extensions.geography,
                    10000
                );
                """
            )
            print("ST_DWithin 10 km grid cell count around Gangtok:", cur.fetchone()[0])

            # 6. Measure real DB size
            cur.execute("SELECT pg_size_pretty(pg_database_size(current_database())), pg_database_size(current_database());")
            pretty_size, raw_bytes = cur.fetchone()
            print(f"Real database size: {pretty_size} ({raw_bytes:,} bytes)")


if __name__ == "__main__":
    main()
