import json
import random
from datetime import datetime
import os
import subprocess
from generate_local_pages import generate_html, load_cities_data, city_state_id

# Archivo de seguimiento de progreso
TRACKER_FILE = 'generation_tracker.json'

# Cargar progreso
def load_tracker():
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, 'r') as file:
            return json.load(file)
    return {'generated_cities': [], 'last_run': None}

# Guardar progreso
def save_tracker(tracker):
    with open(TRACKER_FILE, 'w') as file:
        json.dump(tracker, file)

# Generar página para un lote de ciudades
def generate_batch(cities):
    generated = []
    for city_data in cities:
        file_name = generate_html(city_data['city'], city_data['state'])
        generated.append(file_name)
    return generated

# Ejecutar el generador diario
def run_daily_generation():
    tracker = load_tracker()
    cities = load_cities_data()
    if not cities:
        print('No cities loaded. Ensure uscities.csv is present in the project root.')
        return

    # Build remaining using normalized ids
    remaining_cities = [city for city in cities if city_state_id(city['city'], city['state']) not in tracker.get('generated_cities', [])]

    # Select up to 50 cities (handle case when fewer remain)
    MAX_BATCH = 50
    batch_size = min(MAX_BATCH, len(remaining_cities))
    if batch_size == 0:
        print('No remaining cities to generate.')
        return

    batch = random.sample(remaining_cities, batch_size)
    
    generated_pages = generate_batch(batch)
    
    # Actualizar el progreso
    for city_data in batch:
        tracker['generated_cities'].append(city_state_id(city_data['city'], city_data['state']))
    
    tracker['last_run'] = datetime.now().isoformat()
    save_tracker(tracker)

    print(f"Generated pages: {generated_pages}")

# Main
if __name__ == '__main__':
    run_daily_generation()