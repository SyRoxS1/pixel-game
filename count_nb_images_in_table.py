from dtb_con import get_db_connection

def count_images(number):

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert the image path and game name into the database
    cursor.execute(
        "SELECT count(image_path) FROM image_game_link;",
        (number)
    )
    
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return result[0]
    return None