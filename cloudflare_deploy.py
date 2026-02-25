import zipfile
import os
import requests
from pathlib import Path

CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
CLOUDFLARE_PROJECT_NAME = os.getenv("CLOUDFLARE_PROJECT_NAME")

GENERATED_DIR = "generated_pages"
ZIP_FILE = "generated_pages.zip"

def zip_generated_pages():
    """Crea un archivo ZIP con todos los archivos en el directorio de salida"""
    with zipfile.ZipFile(ZIP_FILE, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in Path(GENERATED_DIR).rglob('*'):
            if file_path.is_file():
                zipf.write(file_path, arcname=file_path.relative_to(GENERATED_DIR))
    print(f"ZIP creado: {ZIP_FILE}")

def deploy_to_cloudflare():
    """Sube el archivo ZIP a Cloudflare Pages vía API"""
    zip_generated_pages()

    url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/pages/projects/{CLOUDFLARE_PROJECT_NAME}/deployments"

    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"
    }

    with open(ZIP_FILE, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, headers=headers, files=files)

    # Depuración: Imprime la respuesta completa
    print(response.status_code)
    print("Result", response.json().get("result", {}))

    # Si la respuesta es exitosa, mostramos la URL de despliegue
    if response.status_code in (200, 201):
        print("✅ Despliegue exitoso!")
        print("URL de despliegue:", response.json().get("result", {}).get("url"))
        print("Respuesta completa:", response.json())
    else:
        print("❌ Error en despliegue:")
        print(response.status_code, response.text)

if __name__ == "__main__":
    deploy_to_cloudflare()
