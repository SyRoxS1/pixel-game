import requests
import os



def dl_image(GAME_ID):
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

    # Set the API endpoint
    url = 'https://api.igdb.com/v4/artworks'

    # IGDB API headers
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }

    # Request body: search by game ID and return the image ID and image_id (slug)
    body = f'fields url, image_id; where game = {GAME_ID};'

    # Make the request
    response = requests.post(url, headers=headers, data=body)

    # Parse the response
    data = response.json()

    if data:
        cover = data[0]
        image_id = cover['image_id']
        # Construct the image URL - choose size from 'thumb', 'cover_small', 'cover_big', etc.
        image_url = f'https://images.igdb.com/igdb/image/upload/t_1080p/{image_id}.jpg'
        img_data = requests.get(image_url).content
        print("Cover Image URL:", image_url)
        with open("images/"+str(GAME_ID)+'.jpg', 'wb') as handler:
            handler.write(img_data)
        return True
    else:
        with open("no_cover.txt","a") as d:
            d.write(str(GAME_ID)+"\n")
        return False



