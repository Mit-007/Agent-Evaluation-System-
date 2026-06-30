import psycopg2
from app.core.config import DB_HOST,DB_PASSWORD,DB_DATABASE,DB_PORT,DB_USER

def get_db_connection():
    """
    Creates and returns a PostgreSQL connection and cursor.
    """
    try:

        if not DB_HOST or not DB_PORT or not DB_DATABASE or not DB_PASSWORD or not DB_USER:
            raise ValueError("not provide DB env values !!")

        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_DATABASE,
            user=DB_USER,
            password=DB_PASSWORD
        )

        cur = conn.cursor()
        return conn, cur
    
    except Exception as e:
        print(f"Database connection failed:  {e}")
        return None, None