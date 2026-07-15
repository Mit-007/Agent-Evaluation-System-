from dotenv import load_dotenv
import os
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")
TEMPERATURE = os.getenv("TEMPERATURE")

DB_HOST = os.getenv("HOST")
DB_PORT = os.getenv("PORT")
DB_DATABASE = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
MIN_CONNECTION_POOLING = int(os.getenv("MIN_CONNECTION_POOLING", 1))
MAX_CONNECTION_POOLING = int(os.getenv("MAX_CONNECTION_POOLING", 10))