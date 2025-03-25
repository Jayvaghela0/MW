from flask import Flask, request, jsonify
from flask_cors import CORS  # CORS Enable karne ke liye
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import cloudscraper  # Cloudflare Bypass ke liye

app = Flask(__name__)
CORS(app)  # API ko all origins ke liye enable karne ke liye

def get_movie_links(movie_name):
    """Google search se movie ke relevant pages ka URL extract karta hai"""
    query = f"{movie_name} site:vegamovies.homes OR site:hdhub4u.mov OR site:7starhdmovies.win"
    results = []

    for url in search(query, num=5, stop=5, pause=2):
        results.append(url)

    return results

def get_download_links(movie_page_url):
    """Vegamovies ya HDHub4u ke pages se real download links extract karta hai"""
    scraper = cloudscraper.create_scraper()
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = scraper.get(movie_page_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        download_links = []
        
        for link in soup.find_all('a', href=True):
            if "https://files" in link['href']:  # Download links ka pattern match karna
                download_links.append(link['href'])
        
        return download_links
    return []

@app.route("/search", methods=["GET"])
def search_movie():
    """Movie search API jo Google se data fetch karegi aur direct links return karegi"""
    movie_name = request.args.get("movie")
    
    if not movie_name:
        return jsonify({"error": "Please provide a movie name"}), 400
    
    movie_links = get_movie_links(movie_name)
    
    if not movie_links:
        return jsonify({"error": "No movie found"}), 404
    
    all_download_links = []
    for link in movie_links:
        all_download_links.extend(get_download_links(link))
    
    return jsonify({"download_links": all_download_links})

if __name__ == "__main__":
    app.run(debug=True)
