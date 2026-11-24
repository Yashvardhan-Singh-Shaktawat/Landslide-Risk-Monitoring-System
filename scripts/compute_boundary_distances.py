"""
Distance-to-Boundary and Uncertainty Audit for LandslideNER
-----------------------------------------------------------
Calculates metric distance to state and district boundaries for every NER event.
Determines if location accuracy radius exceeds distance to boundary.
Evaluates impacts on East Sikkim, Aizawl, Senapati, and Tamenglong.
Prints verifiable raw and cleaned rows for all 17 test cases.
"""

import os
import sys
import csv
import json
import math
from collections import Counter, defaultdict
from shapely.geometry import shape, Point
from shapely.ops import transform
from shapely.prepared import prep

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_CSV = os.path.join(PROJECT_ROOT, "ml", "data", "raw", "Global_Landslide_Catalog_Export.csv")
STATE_GEOJSON = os.path.join(PROJECT_ROOT, "ml", "data", "raw", "boundaries", "india_state.geojson")
DISTRICT_GEOJSON = os.path.join(PROJECT_ROOT, "ml", "data", "raw", "boundaries", "india_district.geojson")

NER_8_STATES = {
    "Arunachal Pradesh", "Assam", "Manipur", "Meghalaya",
    "Mizoram", "Nagaland", "Sikkim", "Tripura"
}

TEST_IDS = [
    "57", "9619", "322", "1108", "3965", "5338", "5430", "5431",
    "4552", "3794", "2261", "1963", "4569", "4571", "3997", "260", "1961"
]

def parse_accuracy_km(acc_str):
    if not acc_str:
        return None
    acc = acc_str.strip().lower()
    if acc in ["exact", "0km"]:
        return 0.0
    if acc.endswith("km"):
        try:
            return float(acc[:-2])
        except ValueError:
            return None
    if acc.endswith("m"):
        try:
            return float(acc[:-1]) / 1000.0
        except ValueError:
            return None
    return None

def compute_distances():
    print("Loading boundaries...")
    with open(STATE_GEOJSON, "r", encoding="utf-8") as f:
        st_data = json.load(f)
    with open(DISTRICT_GEOJSON, "r", encoding="utf-8") as f:
        dist_data = json.load(f)

    # State polygons
    state_polys = {}
    for feat in st_data["features"]:
        name = feat["properties"].get("NAME_1", "").strip()
        geom = shape(feat["geometry"])
        state_polys[name] = {
            "geom": geom,
            "prep": prep(geom)
        }

    # District polygons
    district_polys = []
    for feat in dist_data["features"]:
        st = feat["properties"].get("NAME_1", "").strip()
        dt = feat["properties"].get("NAME_2", "").strip()
        geom = shape(feat["geometry"])
        district_polys.append({
            "state": st,
            "district": dt,
            "geom": geom,
            "prep": prep(geom)
        })

    # Read raw data
    with open(RAW_CSV, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        all_rows = list(reader)

    print(f"Total raw rows: {len(all_rows)}")

    # Metric projection helper: Equirectangular around center (lon0, lat0)
    R = 6371000.0 # earth radius in meters

    def get_metric_distance_to_boundary(pt_lon, pt_lat, polygon_geom):
        # Local equirectangular transform around pt
        cos_lat = math.cos(math.radians(pt_lat))
        def to_m(x, y):
            xm = (x - pt_lon) * math.radians(1) * R * cos_lat
            ym = (y - pt_lat) * math.radians(1) * R
            return xm, ym
        
        # Project polygon boundary
        proj_boundary = transform(to_m, polygon_geom.boundary)
        # Point in local coords is (0, 0)
        pt_m = Point(0, 0)
        dist_m = proj_boundary.distance(pt_m)
        return dist_m / 1000.0 # return km

    cleaned_ner = []
    open_ner = []
    test_cases_data = {}

    for row in all_rows:
        eid = (row.get("event_id") or "").strip()
        import_src = (row.get("event_import_source") or "").strip().lower()
        lat_str = row.get("latitude")
        lon_str = row.get("longitude")

        try:
            lat = float(lat_str)
            lon = float(lon_str)
            pt = Point(lon, lat)
        except Exception:
            continue

        # Find PIP state and district
        pip_state = None
        pip_district = None
        assigned_dist_geom = None

        for d in district_polys:
            if d["prep"].contains(pt):
                pip_state = d["state"]
                pip_district = d["district"]
                assigned_dist_geom = d["geom"]
                break

        if not pip_state:
            for st_name, s_info in state_polys.items():
                if s_info["prep"].contains(pt):
                    pip_state = st_name
                    pip_district = "Unknown District"
                    break

        if pip_state not in NER_8_STATES:
            # Check if it's one of the test IDs anyway
            if eid in TEST_IDS:
                test_cases_data[eid] = {
                    "raw": row,
                    "pip_state": pip_state or "Outside India",
                    "pip_district": pip_district or "None",
                    "dist_state_km": None,
                    "dist_dist_km": None,
                    "state_uncertain": False,
                    "district_uncertain": False
                }
            continue

        # Point is inside NER!
        acc_str = row.get("location_accuracy", "")
        acc_km = parse_accuracy_km(acc_str)

        # Distance to state boundary
        st_geom = state_polys[pip_state]["geom"]
        dist_state_km = get_metric_distance_to_boundary(lon, lat, st_geom)

        # Distance to district boundary
        if assigned_dist_geom:
            dist_dist_km = get_metric_distance_to_boundary(lon, lat, assigned_dist_geom)
        else:
            dist_dist_km = 0.0

        state_uncertain = (acc_km is not None and acc_km > dist_state_km)
        dist_uncertain = (acc_km is not None and acc_km > dist_dist_km)

        processed_entry = {
            "event_id": eid,
            "latitude": lat,
            "longitude": lon,
            "pip_state": pip_state,
            "pip_district": pip_district,
            "location_accuracy": acc_str,
            "acc_km": acc_km,
            "dist_state_km": round(dist_state_km, 2),
            "dist_dist_km": round(dist_dist_km, 2),
            "state_uncertain": state_uncertain,
            "district_uncertain": dist_uncertain,
            "event_date": row.get("event_date", ""),
            "import_source": import_src,
            "event_title": row.get("event_title", ""),
            "location_description": row.get("location_description", ""),
            "admin_division_name": row.get("admin_division_name", "")
        }

        if eid in TEST_IDS:
            test_cases_data[eid] = {
                "raw": row,
                "pip_state": pip_state,
                "pip_district": pip_district,
                "dist_state_km": round(dist_state_km, 2),
                "dist_dist_km": round(dist_dist_km, 2),
                "state_uncertain": state_uncertain,
                "district_uncertain": dist_uncertain
            }

        if import_src == "glc":
            cleaned_ner.append(processed_entry)
        elif import_src != "test":
            open_ner.append(processed_entry)

    print("\n========================================================")
    print("AUDIT RESULTS: CLEANED NER (GLC legacy) ROWS (N = %d)" % len(cleaned_ner))
    print("========================================================")
    
    state_unc_count = sum(1 for r in cleaned_ner if r["state_uncertain"])
    dist_unc_count = sum(1 for r in cleaned_ner if r["district_uncertain"])
    print(f"State assignment uncertain (accuracy > distance to state boundary): {state_unc_count} / {len(cleaned_ner)} ({state_unc_count/len(cleaned_ner)*100:.1f}%)")
    print(f"District assignment uncertain (accuracy > distance to district boundary): {dist_unc_count} / {len(cleaned_ner)} ({dist_unc_count/len(cleaned_ner)*100:.1f}%)")

    # Focus Districts Breakdown
    print("\n--- FOCUS DISTRICTS BREAKDOWN (Cleaned GLC) ---")
    dist_stats = defaultdict(lambda: {"total": 0, "state_unc": 0, "dist_unc": 0, "acc_counts": Counter()})
    for r in cleaned_ner:
        key = (r["pip_state"], r["pip_district"])
        dist_stats[key]["total"] += 1
        if r["state_uncertain"]:
            dist_stats[key]["state_unc"] += 1
        if r["district_uncertain"]:
            dist_stats[key]["dist_unc"] += 1
        dist_stats[key]["acc_counts"][r["location_accuracy"]] += 1

    focus_targets = [
        ("Sikkim", "East"),
        ("Mizoram", "Aizawl"),
        ("Manipur", "Senapati"),
        ("Manipur", "Tamenglong")
    ]

    for st, dt in focus_targets:
        stats = dist_stats.get((st, dt), {"total": 0, "state_unc": 0, "dist_unc": 0, "acc_counts": Counter()})
        print(f"\nDistrict: {st} -> {dt}")
        print(f"  Total Cleaned GLC Events: {stats['total']}")
        print(f"  State Assignment Uncertain: {stats['state_unc']} (accuracy > distance to state border)")
        print(f"  District Assignment Uncertain: {stats['dist_unc']} (accuracy > distance to district border)")
        print(f"  Accuracy Breakdown: {dict(stats['acc_counts'])}")

    # All NER States Summary
    print("\n--- ALL NER STATES SUMMARY (Cleaned GLC) ---")
    state_summary = defaultdict(lambda: {"total": 0, "state_unc": 0, "dist_unc": 0})
    for r in cleaned_ner:
        st = r["pip_state"]
        state_summary[st]["total"] += 1
        if r["state_uncertain"]:
            state_summary[st]["state_unc"] += 1
        if r["district_uncertain"]:
            state_summary[st]["dist_unc"] += 1

    for st in sorted(NER_8_STATES):
        s = state_summary[st]
        print(f"  {st:18s}: {s['total']:3d} events | {s['state_unc']:3d} state uncertain | {s['dist_unc']:3d} district uncertain")

    # Open submissions summary
    print("\n========================================================")
    print("AUDIT RESULTS: CITIZEN / OPEN SUBMISSIONS (N = %d)" % len(open_ner))
    print("========================================================")
    open_state_unc = sum(1 for r in open_ner if r["state_uncertain"])
    open_dist_unc = sum(1 for r in open_ner if r["district_uncertain"])
    print(f"State uncertain: {open_state_unc} / {len(open_ner)}")
    print(f"District uncertain: {open_dist_unc} / {len(open_ner)}")
    open_acc_le_1km = [r for r in open_ner if r["acc_km"] is not None and r["acc_km"] <= 1.0]
    print(f"Submissions with accuracy <= 1km (high confidence validation candidate): {len(open_acc_le_1km)}")
    for r in open_acc_le_1km:
        print(f"  ID {r['event_id']:6s} | {r['pip_state']:10s} | {r['pip_district']:15s} | acc: {r['location_accuracy']} | date: {r['event_date'][:10]} | title: {r['event_title'][:30]}")

    # Output detailed CSV of distance metrics
    out_dist_csv = os.path.join(PROJECT_ROOT, "ml", "data", "processed", "ner_boundary_distance_audit.csv")
    with open(out_dist_csv, "w", newline="", encoding="utf-8") as f:
        headers = [
            "event_id", "import_source", "pip_state", "pip_district", "latitude", "longitude",
            "location_accuracy", "acc_km", "dist_state_km", "dist_dist_km", "state_uncertain", "district_uncertain",
            "event_date", "event_title", "location_description"
        ]
        w = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        w.writeheader()
        w.writerows(cleaned_ner)
        w.writerows(open_ner)

    print(f"\nSaved boundary distance audit to: {out_dist_csv}")

    # Print raw and cleaned for the 17 IDs
    print("\n========================================================")
    print("VERIFIED TABLE FOR 17 TEST IDs (SCRIPT GENERATED)")
    print("========================================================")
    print(f"{'ID':6s} | {'Raw Date':20s} | {'Acc':6s} | {'Lat':8s} | {'Lon':8s} | {'PIP State':16s} | {'PIP District':14s} | {'DistSt(km)':10s} | {'DistDt(km)':10s} | {'StUnc':5s} | {'DtUnc':5s} | {'Raw Title'}")
    print("-" * 150)
    for eid in TEST_IDS:
        info = test_cases_data.get(eid)
        if not info:
            print(f"{eid:6s} | NOT FOUND")
            continue
        raw = info["raw"]
        raw_date = raw.get("event_date", "")[:19]
        acc = raw.get("location_accuracy", "")
        lat = raw.get("latitude", "")[:8]
        lon = raw.get("longitude", "")[:8]
        st = info["pip_state"]
        dt = info["pip_district"]
        dst = str(info["dist_state_km"]) if info["dist_state_km"] is not None else "N/A"
        ddt = str(info["dist_dist_km"]) if info["dist_dist_km"] is not None else "N/A"
        sunc = str(info["state_uncertain"])
        dunc = str(info["district_uncertain"])
        title = raw.get("event_title", "")[:35]
        print(f"{eid:6s} | {raw_date:20s} | {acc:6s} | {lat:8s} | {lon:8s} | {st:16s} | {dt:14s} | {dst:10s} | {ddt:10s} | {sunc:5s} | {dunc:5s} | {title}")

if __name__ == "__main__":
    compute_distances()

