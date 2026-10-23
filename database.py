import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        ssl_disabled=False
    )


if __name__ == "__main__":
    try:
        connection = get_connection()

        if connection.is_connected():
            print("Database connected successfully!")

    except mysql.connector.Error as e:
        print("Database connection failed:", e)

    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()