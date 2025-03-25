from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re
import time
import undetected_chromedriver as uc

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Function to scrape direct movie download link
def get_movie_download_link(search_query):
    try:
        # Google Search to find movie download websites
        google_search_url = f"https://www.google.com/search?q={search_query}+movie+download+site"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(google_search_url, headers=headers)

        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract first 5 result links
        movie_sites = [a["href"] for a in soup.find_all("a", href=True) if "http" in a["href"]][:5]

        # Try each website to extract direct download link
        for site in movie_sites:
            link = scrape_direct_link(site)
            if link:
                return link

        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


# Scraper Function (Handles Both Static & JavaScript-based Sites)
def scrape_direct_link(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract direct download link from static pages
        matches = re.findall(r'https?://[^\s]+?\.mp4', response.text)
        if matches:
            return matches[0]

        # If no direct link found, use JavaScript Execution (Selenium)
        return scrape_js_generated_link(url)
    except Exception as e:
        print(f"Scraping Error: {e}")
        return None


# Handle JavaScript-Generated Links using Selenium
def scrape_js_generated_link(url):
    try:
        options = uc.ChromeOptions()
        options.add_argument("--headless")  # Run in background
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = uc.Chrome(options=options)
        driver.get(url)

        time.sleep(5)  # Wait for JavaScript to load

        links = driver.find_elements("tag name", "a")
        direct_links = [link.get_attribute("href") for link in links if ".mp4" in link.get_attribute("href")]

        driver.quit()

        return direct_links[0] if direct_links else None
    except Exception as e:
        print(f"Selenium Error: {e}")
        return None


# Flask Routes
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
    movie_name = request.form.get("movie_name")

    if not movie_name:
        return jsonify({"error": "Please enter a movie name!"}), 400

    direct_link = get_movie_download_link(movie_name)

    if direct_link:
        return jsonify({"success": True, "direct_link": direct_link})
    else:
        return jsonify({"error": "Download link not found!"}), 404


if __name__ == "__main__":
    app.run(debug=True)
