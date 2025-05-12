import requests

url = "https://jikan.moe/"
response = requests.get(url)

if response.status_code == 200:
    print("API is working")
    print(response.json())
else:
    print("Failed to fetch data:", response.status_code)