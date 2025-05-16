import requests

def fetch_anime_data(endpoint):
    response = requests.get(f'https://api.jikan.moe/v4/{endpoint}')
    response.raise_for_status()
    json_data = response.json()

    if json_data()


