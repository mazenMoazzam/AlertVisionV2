import certifi
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB", "alertvision")

client = MongoClient(MONGO_URI, tls=True, tlsCAFile=certifi.where())

db = client[MONGO_DB]

def get_mongo_collection(name):
    return db[name]

def test_mongo_connection():
    try:
        client.admin.command('ping')
        return "connected"
    except Exception as e:
        return f"error: {e}"
