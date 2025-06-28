from dtb_con import get_db_connection

def search_name(partial):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Use parameterized query with LIKE
    cursor.execute(
        """
        SELECT game_name 
        FROM image_game_link 
        WHERE game_name ILIKE %s 
        ORDER BY game_name 
        LIMIT 10;
        """,
        (f"%{partial}%",)
    )

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return [row[0] for row in results]
