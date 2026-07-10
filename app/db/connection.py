from psycopg2.pool import ThreadedConnectionPool
from app.core.config import (
    DB_HOST,
    DB_PASSWORD,
    DB_DATABASE,
    DB_PORT,
    DB_USER,
)

connection_pool = None

def init_db_pool():
    global connection_pool

    if connection_pool is None:
        connection_pool = ThreadedConnectionPool(
            minconn=2,
            maxconn=10,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_DATABASE,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        
def get_db_connection():
    try:
        if connection_pool is None:
            raise Exception("Connection pool is not initialized.")

        conn = connection_pool.getconn()
        cur = conn.cursor()

        return conn, cur

    except Exception as e:
        print(f"Database connection failed: {e}")
        return None, None
        
        
def release_db_connection(conn, cur=None):
    try:
        if cur:
            cur.close()

        if conn:
            connection_pool.putconn(conn)

    except Exception as e:
        print(f"Error releasing connection: {e}")