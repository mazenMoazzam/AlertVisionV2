import json
from datetime import datetime
from pymongo import MongoClient
from utils.detector import detect_objects
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB", "alertvision")
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

def process_feed(feed_url, mode="object"):
    print(f"🎥 Starting detection for feed: {feed_url}")
    try:
        events = detect_objects(feed_url, max_duration=60, mode=mode)

        result = {
            "feed_url": feed_url,
            "timestamp": datetime.utcnow(),
            "events": events,
            "status": "completed" if events else "no_detections"
        }

        db["detections"].insert_one(result)
        print(f"Stored {len(events)} events for feed {feed_url} in MongoDB.")
    except Exception as e:
        print(f"Error processing {feed_url}: {e}")
        db["detections"].insert_one({
            "feed_url": feed_url,
            "timestamp": datetime.utcnow(),
            "status": "failed",
            "error": str(e)
        })

def process_all_feeds(feeds_file="feeds.json"):
    with open(feeds_file, "r") as f:
        feeds_data = json.load(f)

    feeds = feeds_data.get("feeds", [])
    print(f"🚀 Starting worker for {len(feeds)} feeds...")

    for feed_url in feeds:
        process_feed(feed_url)

    print("All feeds processed. Check MongoDB for results.")

if __name__ == "__main__":
    process_all_feeds()
