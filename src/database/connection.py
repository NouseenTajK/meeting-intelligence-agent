import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI)

try:
    client.admin.command("ping")
    print("Connected to MongoDB successfully 🚀")
except Exception as e:
    print("Connection failed ❌", e)