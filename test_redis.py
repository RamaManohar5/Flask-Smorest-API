import redis
import os

# Load environment variables if not already loaded
from dotenv import load_dotenv
load_dotenv()

# Get Redis URL from environment or default to localhost
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

try:
    # Connect to Redis
    connection = redis.from_url(redis_url)

    # Test the connection
    connection.ping()
    print(f"Successfully connected to Redis at {redis_url}")
except Exception as e:
    print(f"Error connecting to Redis at {redis_url}: {str(e)}")
