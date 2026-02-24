import os
import json
import random
from datetime import datetime

# Cargar los datos de las ciudades
def load_cities_data():
    cities = []
    with open('uscities.csv', 'r') as file:
        for line in file.readlines():
            # Suponiendo que el CSV tiene el formato Ciudad, Estado, Población
            city, state, population = line.strip().split(',')
            if int(population) <= 2500:  # Filtramos por ciudades de menos de 2500 habitantes
                cities.append({'city': city, 'state': state})
    return cities

# Generar HTML para cada ciudad
def generate_html(city, state):
    city_state = f"{city}-{state}"
    file_name = f"generated_pages/{city_state}.html"
    
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