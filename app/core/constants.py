from dotenv import load_dotenv
import os
load_dotenv()


# --> set boundaries for score
BENCHMARK_SCORE_UPPER_LIMIT = 10
BENCHMARK_SCORE_LOWER_LIMIT = 1


# -->  Set Limit for Db connection pooling
MIN_CONNECTION_POOLING = int(os.getenv("MIN_CONNECTION_POOLING"))
MAX_CONNECTION_POOLING = int(os.getenv("MAX_CONNECTION_POOLING"))