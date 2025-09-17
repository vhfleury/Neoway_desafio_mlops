import redis
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))



def get_client():
    client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    return client

def save_hset(client, key: str, mapping: dict):
    client.hset(key, mapping=mapping)
    
def check_redis_connection():
    try:
        client = get_client()
        client.ping()
        logging.info(f"Redis connection successful to {REDIS_HOST}:{REDIS_PORT}")
    except Exception as e:
        logging.error(f"Failed to connect to Redis {e}", exc_info=True)
        raise
