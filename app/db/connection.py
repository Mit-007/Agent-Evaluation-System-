import psycopg2
from app.core.config import DB_HOST,DB_PASSWORD,DB_DATABASE,DB_PORT,DB_USER

conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_DATABASE,
    user=DB_USER,
    password=DB_PASSWORD
)

cur = conn.cursor()
