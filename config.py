import psycopg2
from dotenv import load_dotenv
import os
import  redis;

load_dotenv()  # Load values from .env

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn

# Redis client setup
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True
)

# Redis stream key (replaces REDIS_STREAM)
STREAM_KEY = os.getenv("REDIS_STREAM_KEY", "user_behavior_stream")
