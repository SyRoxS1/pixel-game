import requests
import time
from flask import Flask, request, jsonify
import os

app = Flask(__name__)


if not os.path.exists("secret_tmdb_key"):
    secret = input("Enter your TMDB API Key: ")
    with open("secret_tmdb_key", "w") as f:
        f.write(secret)
with open("secret_tmdb_key", "r") as f:
    TMDB_API_KEY = f.read().strip()

TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"

# Optional: simple in-memory cooldown timer to reduce rate
last_tmdb_call = 0
MIN_INTERVAL = 0.3  # seconds between requests (adjust if needed)

def search_name(query):
    global last_tmdb_call

    # Rate limiting to avoid hitting TMDB limits
    now = time.time()
    if now - last_tmdb_call < MIN_INTERVAL:
        time.sleep(MIN_INTERVAL - (now - last_tmdb_call))

    params = {
        "query": query,
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "page": 1,
        "include_adult": False,
    }

    try:
        response = requests.get(TMDB_SEARCH_URL, params=params, timeout=3)
        response.raise_for_status()
        last_tmdb_call = time.time()
        data = response.json()
        # Return a simplified version of the result
        return [
            {
                "title": movie["title"],
                "id": movie["id"],
                "poster": f"https://image.tmdb.org/t/p/w185{movie['poster_path']}" if movie.get("poster_path") else None,
                "release_date": movie.get("release_date"),
            }
            for movie in data.get("results", [])[:10]
        ]
    except Exception as e:
        print("Error querying TMDB:", e)
        return []


