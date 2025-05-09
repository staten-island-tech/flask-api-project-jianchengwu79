from flask import Flask, render_template
import requests

app = Flask(__name__)

API_BASE = "https://genshin.jmp.blue"

# Home page: list of characters
@app.route("/")
def index():
    try:
        response = requests.get(f"{API_BASE}/characters", timeout=5)
        response.raise_for_status()
        slugs = response.json()
        print(f"Found {len(slugs)} character slugs.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching character list: {e}")
        return "Error loading character list. Please try again later.", 500

    characters = []

    for slug in slugs:
        try:
            char_response = requests.get(f"{API_BASE}/characters/{slug}", timeout=3)
            char_response.raise_for_status()
            char = char_response.json()
            print(f"Fetched {slug}")

            # Try 'card' image, fallback to 'icon'
            images = char.get('images', {})
            image_url = images.get('card') or images.get('icon')

            if not image_url:
                print(f"⚠️ No image found for: {slug}")
                continue

            characters.append({
                'slug': slug,
                'name': char.get('name', slug.title()),
                'image': image_url
            })
        except Exception as e:
            print(f"Error loading character '{slug}': {e}")
            continue

    print(f"Total characters loaded: {len(characters)}")
    return render_template("index.html", characters=characters)


# Character detail page
@app.route("/character/<slug>")
def character_detail(slug):
    try:
        response = requests.get(f"{API_BASE}/characters/{slug}", timeout=5)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching character '{slug}': {e}")
        return f"Error loading character: {slug}", 500

    return render_template("character.html", character={
        'name': data.get('name', slug.title()),
        'slug': slug,
        'image': data['images']['card'],  # You can choose another image type if you prefer
        'vision': data.get('vision', 'Unknown'),
        'weapon': data.get('weapon', 'Unknown'),
        'nation': data.get('nation', 'Unknown'),
        'affiliation': data.get('affiliation', 'Unknown'),
        'birthday': data.get('birthday', 'Unknown'),
        'rarity': data.get('rarity', '?'),
        'description': data.get('description', 'No description available.')
    })

if __name__ == "__main__":
    app.run(debug=True)
