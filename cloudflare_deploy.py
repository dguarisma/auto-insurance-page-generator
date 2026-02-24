import os
import requests

CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CLOUDFLARE_PROJECT_NAME = os.getenv("CLOUDFLARE_PROJECT_NAME")

def deploy_to_cloudflare():
    url = f"https://api.cloudflare.com/client/v4/pages/projects/{CLOUDFLARE_PROJECT_NAME}/deployments"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    files = {
        "files": open("generated_pages/*", "rb")
    }
    response = requests.post(url, headers=headers, files=files)
    if response.status_code == 200:
        print("Despliegue exitoso!")
    else:
        print(f"Error en el despliegue: {response.text}")

deploy_to_cloudflare()