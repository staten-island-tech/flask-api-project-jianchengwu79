import requests

# API URL and parameters
url = "https://api.jikan.moe/v4/top/anime"
params = {
    "type": "tv",       
    "filter": "airing",   
    "rating": "pg13",    
    "sfw": True,           
    "page": 1,               
    "limit": 5               
}

response = requests.get(url, params=params)
data = response.json()


for anime in data.get("data", []):
    title = anime.get("title")
    rating = anime.get("rating")

    if rating in ["r", "rx"]:
        print(f"{title} may not be suitable for all audiences (Rating: {rating.upper()})")
    else:
        print(f"{title} (Rating: {rating.upper()})")
