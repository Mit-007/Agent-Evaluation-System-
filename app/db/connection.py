from psycopg2.pool import ThreadedConnectionPool
from app.core.config import (DB_HOST,DB_PASSWORD,DB_DATABASE,DB_PORT,DB_USER,MAX_CONNECTION_POOLING,MIN_CONNECTION_POOLING)
from app.core.logger import logger

connection_pool = None

def init_db_pool():
    global connection_pool
    
    try:
        if connection_pool is None:
            connection_pool = ThreadedConnectionPool(
                minconn=MIN_CONNECTION_POOLING,
                maxconn=MAX_CONNECTION_POOLING,
                host=DB_HOST,
                port=DB_PORT,
                database=DB_DATABASE,
                user=DB_USER,
                password=DB_PASSWORD,
            )

            logger.debug("Database connection pool initialized successfully.")

    except Exception as e:
        logger.exception(f"Failed to initialize database connection pool: {e}")
        connection_pool = None
        raise
        
def close_db_pool():
    global connection_pool

    try:
        if connection_pool is not None:
            connection_pool.closeall()
            connection_pool = None

            logger.debug("Database connection pool closed successfully.")

    except Exception as e:
        logger.exception(f"Failed to close database connection pool: {e}")
        raise

def get_db_connection():
    try:
        if connection_pool is None:
            raise ConnectionError("Connection pool is not initialized.")

        conn = connection_pool.getconn()

        if not conn:
            raise ConnectionError("Unable to connect to the database.")

        cur = conn.cursor()

        if not cur:
            raise ConnectionError("Unable to create cursor for the database.")
        
        logger.debug(f"connection pool : {conn}")
        return conn, cur
    
    except ConnectionError as e:
        raise 

    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise Exception(f"error in db connection , {e}")
        
        
def release_db_connection(conn, cur=None):
    try:
        if cur:
            cur.close()

        if conn:
            connection_pool.putconn(conn)

        logger.debug(f"connection release : {conn}")

    except Exception as e:
        logger.error(f"Error releasing connection: {e}")
        if conn:
            try :
                conn.close()
            except Exception:
                logger.warning("connection not closed !!")