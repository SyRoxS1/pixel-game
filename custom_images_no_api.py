# Used to import image from folder, the name is the file name without extension
from dtb_instert import insert_image
import os

for filename in os.listdir('import'):
    if filename.endswith(('.jpg', '.png', '.jpeg', '.gif', '.webp')):
        game_name = os.path.splitext(filename)[0] 
        image_path = filename  
        insert_image(game_name, image_path)
    else:
        print(f"Skipping unsupported file type: {filename}")