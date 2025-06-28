import psycopg2

def get_db_connection():
    with open("db_password","r") as f:
        db_password = f.read().strip()
    
    conn = psycopg2.connect(
        dbname="pixel_game",
        user="pixel",
        password=db_password,
        host="10.0.0.15"
    )
    
    
    return conn