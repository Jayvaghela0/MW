from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import cloudscraper
from bs4 import BeautifulSoup
from googlesearch import search

app = Flask(__name__)
CORS(app)  # 🔥 Allow frontend requests

scraper = cloudscraper.create_scraper()  # 🔥 Cloudflare bypass

def google_search(query, max_results=5):
    """Google se top movie download links fetch karega"""
    results = []
    try:
        for url in search(query, stop=max_results):
            results.append(url)
    except Exception as e:
        return {"error": str(e)}
    return results

def get_real_movie_links(url):
    """🔥 Ads & JavaScript redirects bypass karke real download link nikalta hai"""
    try:
        response = scraper.get(url)  # 🔥 Cloudflare bypass request
        soup = BeautifulSoup(response.text, "html.parser")

        # 🔹 Find all links in the page
        all_links = [a["href"] for a in soup.find_all("a", href=True)]

        # 🔥 Filter only actual download links (adjust according to the website)
        download_links = [link for link in all_links if "download" in link.lower()]
        
        return download_links if download_links else ["No direct links found"]

    except Exception as e:
        return [f"Error: {str(e)}"]

@app.route("/search", methods=["GET"])
def search_movie():
    """User se movie name lega, Google se movie links fetch karega, aur real download links dega"""
    movie_name = request.args.get("movie")

    if not movie_name:
        return jsonify({"error": "Please provide a movie name"}), 400

    query = f"{movie_name} site:vegamovies.wiki OR site:hdhub4u.life OR site:7starhd.bio"
    movie_sites = google_search(query)

    if "error" in movie_sites:
        return jsonify({"error": "Failed to fetch movie links"}), 500

    # 🔥 Get actual download links from each movie site
    final_links = {}
    for site in movie_sites:
        final_links[site] = get_real_movie_links(site)

    return jsonify({"download_links": final_links})

if __name__ == "__main__":
    app.run(debug=True)


