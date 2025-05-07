from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def home():
    try:
        response = requests.get("https://genshin.dev/characters")
        response.raise_for_status()
        all_characters = response.json()
        limited_characters = all_characters[:5]
        return render_template("home.html", characters=limited_characters)
    except Exception as e:
        return render_template("error.html", message="Failed to load characters.")


@app.route("/character/<name>")
def character_page(name):
    try:
        response = requests.get(f"https://genshin.dev/characters/{name.lower()}")
        if response.status_code != 200:
            return render_template("error.html", message="Character not found.")
        character_data = response.json()
        image_url = f"https://genshin.dev/characters/{name.lower()}/icon"
        return render_template("character.html", data=character_data, name=name, image=image_url)
    except Exception as e:
        return render_template("error.html", message="Something went wrong.")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        char_name = request.form["char_name"]
        return character_page(char_name)
    return render_template("search.html")

if __name__ == '__main__':
    app.run(debug=True)
