import os
import json
import random
import csv
from datetime import datetime


# Cargar los datos de las ciudades
def load_cities_data():
    cities = []
    csv_path = 'uscities.csv'

    if not os.path.exists(csv_path):
        print(f"File not found: {csv_path}")
        return cities

    with open(csv_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        # Leer posible encabezado
        header = next(reader, None)
        city_idx = 0
        state_idx = 2
        pop_idx = 8

        if header:
            low = [h.lower() for h in header]
            for name in ('city', 'city_ascii'):
                if name in low:
                    city_idx = low.index(name)
                    break
            for name in ('state_id', 'state', 'state_name'):
                if name in low:
                    state_idx = low.index(name)
                    break
            for name in ('population', 'pop'):
                if name in low:
                    pop_idx = low.index(name)
                    break

        for row in reader:
            # Ignorar filas vacías
            if not row or not any(cell.strip() for cell in row):
                continue

            try:
                city = row[city_idx].strip() if len(row) > city_idx else ''
                state = row[state_idx].strip() if len(row) > state_idx else ''
                pop_raw = row[pop_idx].strip() if len(row) > pop_idx else '0'

                # Limpieza de población (puede contener comas)
                pop_clean = pop_raw.replace('"', '').replace(',', '')
                population = int(float(pop_clean)) if pop_clean else 0

                if not city:
                    raise ValueError('missing city')

                cities.append({'city': city, 'state': state, 'population': population})
            except Exception as e:
                print(f"Warning: skipping invalid line: {row} ({e})")

    return cities

# Generar HTML para cada ciudad
def generate_html(city, state):
    # Normalizar nombre de archivo
    safe_city = ''.join(c for c in city if c.isalnum() or c in (' ', '-', '_')).strip().replace(' ', '_')
    safe_state = ''.join(c for c in state if c.isalnum() or c in (' ', '-', '_')).strip().replace(' ', '_')
    city_state = f"{safe_city}-{safe_state}"
    out_dir = 'generated_pages'
    os.makedirs(out_dir, exist_ok=True)
    file_name = f"{out_dir}/{city_state}.html"
    
    content = f"""
    <html>
    <head>
        <title>Auto Insurance in {city}, {state}</title>
        <meta name="description" content="Affordable auto insurance in {city}, {state}. Compare rates today!">
    </head>
    <body>
        <h1>Get Auto Insurance in {city}, {state}</h1>
        <p>Find affordable auto insurance in {city}. Contact us for free quotes.</p>
        <footer>
            <p>Contact us at 1-800-123-4567</p>
        </footer>
    </body>
    </html>
    """

    # Guardar el archivo HTML
    with open(file_name, 'w') as file:
        file.write(content)

    return file_name

# Main: Generar páginas
def main():
    cities = load_cities_data()
    
    for city_data in cities:
        file_name = generate_html(city_data['city'], city_data['state'])
        print(f"Page generated: {file_name}")

if __name__ == '__main__':
    main()