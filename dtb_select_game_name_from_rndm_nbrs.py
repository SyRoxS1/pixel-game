from dtb_con import get_db_connection

def select_name(number):

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert the image path and game name into the database
    cursor.execute(
        "SELECT game_name FROM image_game_link ORDER BY image_path LIMIT 1 OFFSET %s;",
        (number,)
    )

    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return result[0]
    return None