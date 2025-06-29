from dtb_con import get_db_connection

def insert_image(game_name, image_path):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the image path or game already exists
    cursor.execute(
        "SELECT 1 FROM image_game_link WHERE image_path = %s AND game_name = %s",
        (image_path, game_name)
    )
    
    exists = cursor.fetchone()
    if exists:
        print(f"Skipping duplicate: {game_name} ({image_path}) already in DB.")
    else:
        cursor.execute(
            "INSERT INTO image_game_link (image_path, game_name) VALUES (%s, %s)",
            (image_path, game_name)
        )
        conn.commit()
        print(f"Inserted: {game_name} ({image_path})")

    cursor.close()
    conn.close()
