import json
import random
from datetime import datetime
import os
import shutil
from pathlib import Path
from generate_local_pages import generate_html, load_cities_data, city_state_id

TRACKER_FILE = 'generation_tracker.json'
OUTPUT_DIR = Path("generated_pages")

def load_tracker():
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, 'r') as file:
            return json.load(file)
    return {'generated_cities': [], 'last_run': None}

def save_tracker(tracker):
    with open(TRACKER_FILE, 'w') as file:
        json.dump(tracker, file)

def clean_output_dir():
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_batch(cities):
    generated = []
    for city_data in cities:
        file_name = generate_html(city_data['city'], city_data['state'])
        generated.append(file_name)
    return generated

def create_index(generated_pages):
    items = "\n".join(
        f'<li><a href="{Path(page).name}">{Path(page).name}</a></li>'
        for page in generated_pages
    )

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Auto Insurance Pages</title>
</head>
<body>
  <h1>Generated Auto Insurance Pages</h1>
  <p>Last build: {datetime.now().isoformat()}</p>
  <ul>
    {items}
  </ul>
</body>
</html>
"""
    with open(OUTPUT_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(html)

def run_daily_generation():
    clean_output_dir()

    tracker = load_tracker()
    cities = load_cities_data()
    if not cities:
        print('No cities loaded. Ensure uscities.csv is present in the project root.')
        create_index([])
        return

    remaining_cities = [
        city for city in cities
        if city_state_id(city['city'], city['state']) not in tracker.get('generated_cities', [])
    ]

    MAX_BATCH = 50
    batch_size = min(MAX_BATCH, len(remaining_cities))

    if batch_size == 0:
        print('No remaining cities to generate.')
        create_index([])
        return

    batch = random.sample(remaining_cities, batch_size)
    generated_pages = generate_batch(batch)

    for city_data in batch:
        tracker['generated_cities'].append(city_state_id(city_data['city'], city_data['state']))

    tracker['last_run'] = datetime.now().isoformat()
    save_tracker(tracker)

    create_index(generated_pages)

    print(f"Generated pages: {generated_pages}")

if __name__ == '__main__':
    run_daily_generation()
