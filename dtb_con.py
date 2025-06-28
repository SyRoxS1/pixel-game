import psycopg2
import os

def get_db_connection():
    if not os.path.exists("db_password"):
        db_password = input("Enter your database password: ")
        with open("db_password", "w") as f:
            f.write(db_password)
            
    with open("db_password","r") as f:
        db_password = f.read().strip()

    conn = psycopg2.connect(
        dbname="pixel_game",
        user="pixel",
        password=db_password,
        host="10.0.0.15"
    )


    return conn