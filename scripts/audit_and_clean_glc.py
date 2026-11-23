"""
NASA Global Landslide Catalog (GLC) — Rigorous Point-in-Polygon (PIP) Audit and Cleaning
----------------------------------------------------------------------------------------
- Source: ml/data/raw/Global_Landslide_Catalog_Export.csv
- Boundary Source: GADM / Datameet India (india_state.geojson, india_district.geojson)
- Assigns state and district via genuine Shapely point-in-polygon containment
- Filters test imports, flags coordinate/description disagreements, assigns event_groups
- Generates exact statistics for date precision, location accuracy, and settings
"""

import os
import sys
import csv
import json
from collections import Counter, defaultdict
from datetime import datetime
from shapely.geometry import shape, Point
from shapely.prepared import prep

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_CSV = os.path.join(PROJECT_ROOT, "ml", "data", "raw", "Global_Landslide_Catalog_Export.csv")
STATE_GEOJSON = os.path.join(PROJECT_ROOT, "ml", "data", "raw", "boundaries", "india_state.geojson")
DISTRICT_GEOJSON = os.path.join(PROJECT_ROOT, "ml", "data", "raw", "boundaries", "india_district.geojson")

PROCESSED_DIR = os.path.join(PROJECT_ROOT, "ml", "data", "processed")
CLEANED_NER_CSV = os.path.join(PROCESSED_DIR, "ner_landslides_cleaned.csv")
OUTSIDE_NER_CSV = os.path.join(PROCESSED_DIR, "outside_ner_landslides.csv")
EXCLUDED_CSV = os.path.join(PROCESSED_DIR, "excluded_test_rows.csv")
FLAGGED_CSV = os.path.join(PROCESSED_DIR, "flagged_disagreements.csv")

NER_8_STATES = {
    "Arunachal Pradesh", "Assam", "Manipur", "Meghalaya",
    "Mizoram", "Nagaland", "Sikkim", "Tripura"
}

TEST_CASES = [
    "322", "1108", "3965", "5312", "5338", "3916", "5430", "5431",
    "4552", "3794", "3805", "7138", "2261", "1963", "4569", "4571",
    "3997", "260", "141", "1961", "221", "133"
]


def load_boundaries():
    print("Loading state and district boundaries...")
    with open(STATE_GEOJSON, "r", encoding="utf-8") as f:
        st_data = json.load(f)
    with open(DISTRICT_GEOJSON, "r", encoding="utf-8") as f:
        dist_data = json.load(f)

    # Prepare state geometries
    states = []
    for feat in st_data["features"]:
        geom = shape(feat["geometry"])
        name = feat["properties"].get("NAME_1", "").strip()
        states.append({"name": name, "geom": geom, "prep": prep(geom)})

    # Prepare district geometries
    districts = []
    for feat in dist_data["features"]:
        geom = shape(feat["geometry"])
        st_name = feat["properties"].get("NAME_1", "").strip()
        dist_name = feat["properties"].get("NAME_2", "").strip()
        districts.append({
            "state": st_name,
            "district": dist_name,
            "geom": geom,
            "prep": prep(geom)
        })

    print(f"Loaded {len(states)} states and {len(districts)} districts.")
    return states, districts


def parse_date(date_str):
    if not date_str:
        return None, "unknown", None
    date_str = date_str.strip()
    # NASA GLC formats: "07/22/2009 12:00:00 AM", "07/22/2009 05:40:00 AM", "07/22/2009"
    for fmt in [
        "%m/%d/%Y %I:%M:%S %p",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y %I:%M %p",
        "%m/%d/%Y %H:%M",
        "%m/%d/%Y"
    ]:
        try:
            dt = datetime.strptime(date_str, fmt)
            # Check if time is 12:00:00 AM (often default placeholder for day precision)
            precision = "day"
            return dt, precision, dt.year
        except ValueError:
            pass
    # If partial
    try:
        parts = date_str.split("/")
        if len(parts) == 3:
            return None, "day", int(parts[2][:4])
        elif len(parts) == 2:
            return None, "month", int(parts[1][:4])
    except Exception:
        pass
    return None, "unknown", None


def main():
    states, districts = load_boundaries()
    
    # Track old normalized_state labels from previous script
    old_labels = {}
    old_csv = os.path.join(PROCESSED_DIR, "ner_landslides_glc.csv")
    if os.path.exists(old_csv):
        with open(old_csv, "r", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                old_labels[row["event_id"]] = row.get("normalized_state", "Unknown")

    print(f"Reading raw data from: {RAW_CSV}")
    with open(RAW_CSV, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        all_rows = list(reader)

    print(f"Total raw rows in NASA GLC: {len(all_rows)}")

    excluded_test_rows = []
    cleaned_ner_rows = []
    outside_ner_rows = []
    flagged_disagreements = []

    # Mapping for event_group: (source_link, event_date) -> group_id
    group_map = {}
    group_counter = 1

    # Statistics accumulators
    ner_state_counts = Counter()
    ner_district_counts = defaultdict(Counter)
    date_precision_counts = Counter()
    year_histogram = Counter()
    dates_list = []
    accuracy_counts = Counter()
    setting_counts = Counter()
    label_change_count = 0

    test_case_results = []

    for row in all_rows:
        eid = row.get("event_id", "")
        country = (row.get("country_name") or "").strip()
        import_source = (row.get("event_import_source") or "").strip().lower()
        lat_str = row.get("latitude")
        lon_str = row.get("longitude")
        admin_gazetteer = (row.get("admin_division_name") or "").strip()
        loc_desc = (row.get("location_description") or "").strip()
        date_str = row.get("event_date") or ""
        source_link = (row.get("source_link") or "").strip()
        accuracy = (row.get("location_accuracy") or "unknown").strip().lower()
        setting = (row.get("landslide_setting") or "unknown").strip().lower()

        # Step 3: Check for test rows (import source != 'glc')
        if import_source != "glc":
            row["exclusion_reason"] = f"event_import_source='{import_source}' (non-glc / test import)"
            excluded_test_rows.append(row)
            continue

        # Parse coordinates
        try:
            lat = float(lat_str)
            lon = float(lon_str)
            pt = Point(lon, lat)
        except (ValueError, TypeError):
            row["exclusion_reason"] = "Invalid coordinates"
            excluded_test_rows.append(row)
            continue

        # Step 2: Point-in-polygon state assignment
        pip_state = None
        for s in states:
            if s["prep"].contains(pt):
                pip_state = s["name"]
                break

        # Point-in-polygon district assignment
        pip_district = None
        if pip_state:
            for d in districts:
                if d["state"] == pip_state and d["prep"].contains(pt):
                    pip_district = d["district"]
                    break
            # Fallback across all districts if state boundary had minor edge discrepancy
            if not pip_district:
                for d in districts:
                    if d["prep"].contains(pt):
                        pip_district = d["district"]
                        if not pip_state:
                            pip_state = d["state"]
                        break

        # Dates & Precision (Step 5)
        dt_val, precision, year = parse_date(date_str)
        if dt_val:
            dates_list.append(dt_val)
        row["date_precision"] = precision
        row["parsed_year"] = str(year) if year else "unknown"

        # Event Grouping (Step 4)
        group_key = (source_link, date_str[:10] if len(date_str) >= 10 else date_str)
        if group_key not in group_map:
            group_map[group_key] = f"GRP_{group_counter:04d}"
            group_counter += 1
        row["event_group"] = group_map[group_key]

        row["pip_state"] = pip_state or "Outside India / Unknown"
        row["pip_district"] = pip_district or "Unknown"

        # Check Disagreements between PIP and Description (Step 2 & 3)
        disagreement_flags = []
        loc_lower = loc_desc.lower()
        for ner_s in NER_8_STATES:
            if ner_s.lower() in loc_lower and pip_state != ner_s:
                disagreement_flags.append(f"Description names '{ner_s}' but coordinates fall in '{pip_state}'")
        
        # Check if gazetteer strongly conflicts
        if admin_gazetteer and pip_state and admin_gazetteer.lower() != pip_state.lower():
            if any(s.lower() == admin_gazetteer.lower() for s in NER_8_STATES):
                disagreement_flags.append(f"Gazetteer names '{admin_gazetteer}' but coordinates fall in '{pip_state}'")

        row["disagreement_flags"] = "; ".join(disagreement_flags)
        if disagreement_flags:
            flagged_disagreements.append(row)

        # Check Test Cases
        if eid in TEST_CASES:
            test_case_results.append({
                "id": eid,
                "lat": lat,
                "lon": lon,
                "admin_gazetteer": admin_gazetteer,
                "location_desc": loc_desc[:80],
                "old_label": old_labels.get(eid, "N/A"),
                "pip_state": pip_state,
                "pip_district": pip_district,
                "flags": row["disagreement_flags"]
            })

        # Track old label vs new label change
        if eid in old_labels:
            if old_labels[eid] != pip_state:
                label_change_count += 1

        # Classify into Cleaned NER vs Outside NER
        if pip_state in NER_8_STATES:
            cleaned_ner_rows.append(row)
            ner_state_counts[pip_state] += 1
            ner_district_counts[pip_state][pip_district] += 1
            date_precision_counts[precision] += 1
            if year:
                year_histogram[year] += 1
            accuracy_counts[accuracy] += 1
            setting_counts[setting] += 1
        else:
            # Check if it was in the old 442 set or near NER
            outside_ner_rows.append(row)

    # Save output files
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    
    out_headers = list(fieldnames) + [
        "pip_state", "pip_district", "date_precision", "parsed_year", "event_group", "disagreement_flags"
    ]

    with open(CLEANED_NER_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=out_headers)
        writer.writeheader()
        writer.writerows(cleaned_ner_rows)

    with open(OUTSIDE_NER_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=out_headers)
        writer.writeheader()
        writer.writerows(outside_ner_rows)

    with open(EXCLUDED_CSV, "w", newline="", encoding="utf-8") as f:
        ex_headers = list(fieldnames) + ["exclusion_reason"]
        writer = csv.DictWriter(f, fieldnames=ex_headers)
        writer.writeheader()
        writer.writerows(excluded_test_rows)

    with open(FLAGGED_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=out_headers)
        writer.writeheader()
        writer.writerows(flagged_disagreements)

    # Calculate independent event groups in cleaned NER
    ner_groups = set(r["event_group"] for r in cleaned_ner_rows)

    print("\n================== AUDIT REPORT ==================")
    print(f"Total raw GLC rows evaluated: {len(all_rows)}")
    print(f"Total test/non-glc rows excluded: {len(excluded_test_rows)}")
    print(f"Total verified rows inside 8 NER States (PIP): {len(cleaned_ner_rows)}")
    print(f"Total independent event groups in NER: {len(ner_groups)} (across {len(cleaned_ner_rows)} rows)")
    print(f"Total rows outside 8 NER states: {len(outside_ner_rows)}")
    print(f"Total flagged coordinate/description disagreements: {len(flagged_disagreements)}")
    print(f"Rows from old 442-row set that changed state label: {label_change_count}")

    print("\n--- 1. REAL NER EVENT COUNTS PER STATE (Point-In-Polygon) ---")
    for st in sorted(NER_8_STATES):
        print(f"  {st:20s}: {ner_state_counts[st]:3d} events")

    print("\n--- 2. DISTRICT BREAKDOWN FOR SIKKIM & CANDIDATE STUDY AREAS ---")
    print(f"All Sikkim Districts (Total = {ner_state_counts['Sikkim']}):")
    for dist, cnt in ner_district_counts["Sikkim"].most_common():
        print(f"    - {dist:15s}: {cnt:2d} events")

    print(f"\nMizoram Districts (Total = {ner_state_counts['Mizoram']}):")
    for dist, cnt in ner_district_counts["Mizoram"].most_common():
        print(f"    - {dist:15s}: {cnt:2d} events")

    print(f"\nManipur Districts (Total = {ner_state_counts['Manipur']}):")
    for dist, cnt in ner_district_counts["Manipur"].most_common():
        print(f"    - {dist:15s}: {cnt:2d} events")

    print(f"\nAssam Districts (Top 5) (Total = {ner_state_counts['Assam']}):")
    for dist, cnt in ner_district_counts["Assam"].most_common(5):
        print(f"    - {dist:15s}: {cnt:2d} events")

    print("\n--- 3. LOCATION ACCURACY BREAKDOWN (NER Cleaned) ---")
    for acc, cnt in accuracy_counts.most_common():
        pct = (cnt / len(cleaned_ner_rows)) * 100
        print(f"  {acc:10s}: {cnt:3d} events ({pct:5.1f}%)")

    print("\n--- 4. SETTING & REPORTING BIAS BREAKDOWN (NER Cleaned) ---")
    for setg, cnt in setting_counts.most_common():
        pct = (cnt / len(cleaned_ner_rows)) * 100
        print(f"  {setg:15s}: {cnt:3d} events ({pct:5.1f}%)")

    print("\n--- 5. DATE PRECISION & TEMPORAL RANGE ---")
    print(f"Date Precision: {dict(date_precision_counts)}")
    if dates_list:
        print(f"Earliest Event Date: {min(dates_list).strftime('%Y-%m-%d')}")
        print(f"Latest Event Date:   {max(dates_list).strftime('%Y-%m-%d')}")
    print("\nPer-Year Histogram (NER Events):")
    for yr in sorted(year_histogram.keys()):
        print(f"  {yr}: {year_histogram[yr]:2d} events")

    print("\n--- 6. EVALUATION OF 22 SPECIFIC TEST CASES ---")
    for tc in test_case_results:
        print(f"ID {tc['id']:4s} | ({tc['lat']:.4f}, {tc['lon']:.4f}) | Old: {tc['old_label']:18s} -> New: {tc['pip_state']:18s} ({tc['pip_district']})")
        if tc["flags"]:
            print(f"        FLAG: {tc['flags']}")
        print(f"        Loc:  {tc['location_desc']}")

    print(f"\n--- 7. EXCLUDED TEST ROWS (Total: {len(excluded_test_rows)}) ---")
    test_ids_to_check = ["6105", "6200", "5250", "4378", "4446", "4798", "4860"]
    print("Requested test IDs check:")
    for ex in excluded_test_rows:
        if ex.get("event_id") in test_ids_to_check:
            print(f"  ID {ex.get('event_id')}: source='{ex.get('event_import_source')}' | title='{ex.get('event_title', '')[:40]}' | loc='{ex.get('location_description', '')[:50]}'")


if __name__ == "__main__":
    main()
