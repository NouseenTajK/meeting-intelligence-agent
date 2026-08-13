import os
from pathlib import Path
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv


# Find the project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Load .env from project root
load_dotenv(BASE_DIR / ".env")


MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION")


if not MONGODB_URI:
    raise ValueError("MONGODB_URI is not set in the .env file")

if not MONGODB_DATABASE:
    raise ValueError("MONGODB_DATABASE is not set in the .env file")

if not MONGODB_COLLECTION:
    raise ValueError("MONGODB_COLLECTION is not set in the .env file")


client = MongoClient(
    MONGODB_URI,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=20000,
)


try:
    client.admin.command("ping")
    print("MongoDB connected successfully!")
except Exception as e:
    raise ConnectionError(f"Could not connect to MongoDB: {e}")


db = client[MONGODB_DATABASE]
meetings_collection = db[MONGODB_COLLECTION]