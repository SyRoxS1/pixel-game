import requests
import json
import time
from artwork import dl_image
from dtb_instert import insert_image
import os

if not os.path.exists("secret_client_id"):
    secret = input("Enter your IGDB Client ID: ")
    with open("secret_client_id", "w") as f:
        f.write(secret)

if not os.path.exists("secret_client_key"):
    secret = input("Enter your IGDB Access Token: ")
    with open("secret_client_key", "w") as f:
        f.write(secret)

with open("secret_client_id","r") as f:
    CLIENT_ID = f.read().strip()
    
with open("secret_client_key","r") as f:
    ACCESS_TOKEN = f.read().strip()

url = "https://api.igdb.com/v4/games"
headers = {
    'Client-ID': CLIENT_ID,
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'text/plain'  # important: plain text, not json
}

all_games = []
offset = 0
limit = 500  # Max allowed per IGDB request

ALLOWED_PLATFORMS = {130, 508}  # Switch and Switch 2

while True:
    # Loose filter: games that have platform 130 or 508 (including others)
    payload = (
        'fields id,name,category,platforms;'
        ' where platforms != null'
        ' & (platforms = [130] | platforms = [508] | platforms = [130, 508] | platforms = [508, 130]);'
        f' limit {limit}; offset {offset};'
    )
    
    response = requests.post(url, headers=headers, data=payload)

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        break

    games = response.json()
    if not games:
        break  # No more results

    # Filter locally: keep only games exclusive to platforms in ALLOWED_PLATFORMS
    filtered_games = []
    for game in games:
        platforms = set(game.get("platforms", []))
        # Only keep if all platforms in ALLOWED_PLATFORMS and length matches
        if platforms and platforms.issubset(ALLOWED_PLATFORMS):
            filtered_games.append(game)

    if not filtered_games:
        # If no filtered results, maybe we're done
        break

    all_games.extend(filtered_games)
    offset += limit

    time.sleep(0.25)  # Respect rate limit (4 requests/sec)

for game in all_games:
    game_id = game["id"]
    game_name = game["name"]
    if os.path.exists(f"images/{game_id}.jpg"):
        insert_image(game_name, f"{game_id}.jpg")
        continue
    downloading = dl_image(game_id)
    if downloading:
        print(f"Downloaded image for {game_name} (ID: {game_id})")
        insert_image(game_name, f"{game_id}.jpg")
    else:
        print(f"No image found for {game_name} (ID: {game_id})")
