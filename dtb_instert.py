from dtb_con import get_db_connection

def insert_image(game_name, image_path):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert the image path and game name into the database
    cursor.execute(
        "INSERT INTO image_game_link (image_path, game_name) VALUES (%s, %s)",
        (image_path, game_name)
    )
    
    # Commit the transaction
    conn.commit()
    
    # Close the cursor and connection
    cursor.close()
    conn.close()
