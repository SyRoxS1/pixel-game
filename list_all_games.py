import requests
import json
import time
from artwork import dl_image

with open("secret_client_id","r") as f:
    CLIENT_ID = f.read().strip()
    
with open("secret_client_key","r") as f:
    ACCESS_TOKEN = f.read().strip()

url = "https://api.igdb.com/v4/games"
headers = {
    'Client-ID': CLIENT_ID,
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

all_games = []
offset = 0
limit = 500  # Max allowed per IGDB request

while True:
    payload = f"fields id,name,category,platforms; where platforms = 130; limit {limit}; offset {offset};"
    response = requests.post(url, headers=headers, data=payload)

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        break

    games = response.json()
    if not games:
        break  # No more results

    all_games.extend(games)
    offset += limit
    time.sleep(0.25)  # Respect rate limit (4 requests/sec)

for game in all_games:
    game_id = game["id"]
    game_name = game["name"]
    print(f"Game ID: {game_id}, Name: {game_name}")
    dl_image(game_id)
