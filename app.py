from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)


def fetch_anime_data(endpoint):
    try:
        response = requests.get(f'https://api.jikan.moe/v4/{endpoint}')
        response.raise_for_status()
        json_data = response.json()

 
        return json_data.get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"[API Error] {e}")
        return []


@app.route('/')
def home():
    anime_list = fetch_anime_data('top/anime')
    if anime_list:
        return render_template('index.html', anime_list=anime_list)
    return render_template('404.html')


@app.route('/search')
def search():
    query = request.args.get('query')
    if query:
        search_results = fetch_anime_data(f'anime?q={query}&limit=10')
        if search_results:
            return render_template('search_results.html', query=query, anime_list=search_results)
    return redirect(url_for('home'))
    

@app.route('/anime/<int:anime_id>')
def anime_detail(anime_id):
    anime = fetch_anime_data(f'anime/{anime_id}')
    if anime:
        return render_template('anime_detail.html', anime=anime)                   
    return render_template('404.html')


@app.route('/genre/<int:genre_id>')
def genre_filter(genre_id):
    genre_anime = fetch_anime_data(f'anime?genres={genre_id}')
    if genre_anime:
        return render_template('search_results.html', anime_list=genre_anime)
    return render_template('404.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
