from fastapi import APIRouter, Query
from utils.db import get_mongo_collection

router = APIRouter()
collection = get_mongo_collection("detections")

@router.get("/")
def get_detections(feed_url: str = None, limit: int = 10):
    query = {}
    if feed_url:
        query["feed_url"] = feed_url
    results = list(collection.find(query).sort("timestamp", -1).limit(limit))
    for r in results:
        r["_id"] = str(r["_id"])
    return results
