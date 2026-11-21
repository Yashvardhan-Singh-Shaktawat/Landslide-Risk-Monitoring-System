"""
Fetch and filter NASA Global Landslide Catalog (GLC) events for North Eastern Region (NER) of India.
Produces a clean, verified CSV artifact in ml/data/processed/ner_landslides_glc.csv.
"""
import urllib.request
import csv
import io
import os
from collections import Counter

URL = "https://data.nasa.gov/docs/legacy/Global_Landslide_Catalog_Export/Global_Landslide_Catalog_Export_rows.csv"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ml", "data", "processed")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "ner_landslides_glc.csv")

NER_STATES = {
    "arunachal pradesh": "Arunachal Pradesh",
    "arunāchal pradesh": "Arunachal Pradesh",
    "assam": "Assam",
    "manipur": "Manipur",
    "meghalaya": "Meghalaya",
    "meghālaya": "Meghalaya",
    "mizoram": "Mizoram",
    "nagaland": "Nagaland",
    "nāgāland": "Nagaland",
    "sikkim": "Sikkim",
    "tripura": "Tripura"
}

# NER Bounding box approximation (including contiguous Himalayan sub-basin corridors)
MIN_LAT, MAX_LAT = 21.5, 29.5
MIN_LON, MAX_LON = 88.0, 97.5


def run_ingestion():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Connecting to NASA Open Data: {URL}...")
    req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    
    saved_rows = []
    state_counter = Counter()
    trigger_counter = Counter()
    fatalities_total = 0
    date_precision_counter = Counter()

    with urllib.request.urlopen(req, timeout=60) as resp:
        text_stream = io.TextIOWrapper(resp, encoding='utf-8', errors='replace')
        reader = csv.DictReader(text_stream)
        headers = reader.fieldnames

        for row in reader:
            country = (row.get('country_name') or '').strip().lower()
            admin_division = (row.get('admin_division_name') or '').strip().lower()
            location_desc = (row.get('location_description') or '').strip().lower()

            if 'india' not in country:
                continue

            matched_state = None
            for key, val in NER_STATES.items():
                if key in admin_division or key in location_desc:
                    matched_state = val
                    break

            lat_str = row.get('latitude')
            lon_str = row.get('longitude')
            
            # Fallback coordinate bbox check
            if not matched_state and lat_str and lon_str:
                try:
                    lat = float(lat_str)
                    lon = float(lon_str)
                    if MIN_LAT <= lat <= MAX_LAT and MIN_LON <= lon <= MAX_LON:
                        # Adjacent coordinate match
                        admin_name = row.get('admin_division_name') or 'NER Border'
                        matched_state = f"NER Border ({admin_name})"
                except ValueError:
                    pass

            if matched_state:
                state_counter[matched_state] += 1
                row['normalized_state'] = matched_state
                saved_rows.append(row)
                
                # Metrics tracking
                trigger = row.get('landslide_trigger') or 'unknown'
                trigger_counter[trigger] += 1
                
                date_val = row.get('event_date') or ''
                if len(date_val) > 10:
                    date_precision_counter['exact_timestamp'] += 1
                elif len(date_val) > 0:
                    date_precision_counter['date_only'] += 1
                else:
                    date_precision_counter['missing'] += 1

                try:
                    fatalities_total += int(row.get('fatality_count') or 0)
                except ValueError:
                    pass

    # Write filtered output
    if saved_rows:
        out_headers = ['normalized_state'] + [h for h in headers if h != 'normalized_state']
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=out_headers)
            writer.writeheader()
            writer.writerows(saved_rows)

    print(f"\n[DONE] Saved {len(saved_rows)} verified NER landslide events to: {OUTPUT_FILE}")
    print("\n--- Event Distribution by State ---")
    for state, count in state_counter.most_common():
        print(f"  {state}: {count}")

    print("\n--- Primary Triggers ---")
    for tr, cnt in trigger_counter.most_common(5):
        print(f"  {tr}: {cnt}")

    print(f"\nTotal Recorded Fatalities: {fatalities_total}")
    print(f"Date Precision Breakdown: {dict(date_precision_counter)}")


if __name__ == "__main__":
    run_ingestion()
