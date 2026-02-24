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

    processed = 0
    skipped = 0
    with open(csv_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        # Intentar detectar si hay encabezado inspeccionando la primera fila
        first_row = next(reader, None)
        header = None
        city_idx = 0
        state_idx = 2
        pop_idx = 8

        rows_iter = reader

        if first_row:
            low_first = [c.lower() for c in first_row]
            if any(name in ''.join(low_first) for name in ('city', 'state', 'population', 'pop')):
                header = first_row
                # reconstruir índices desde el encabezado
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
            else:
                # No hay encabezado: procesar la primera fila como dato
                rows_iter = [first_row] + list(reader)

        for row in rows_iter:
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
                processed += 1
            except Exception as e:
                skipped += 1
                print(f"Warning: skipping invalid line: {row} ({e})")

    print(f"Cities processed: {processed}. Lines skipped: {skipped}.")
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