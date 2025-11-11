from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.mq import publish_feed

router = APIRouter()

class FeedRequest(BaseModel):
    feed_url: str

@router.post("/enqueue")
def enqueue_feed(request: FeedRequest):
    try:
        publish_feed(request.feed_url)
        return {"message": f"Feed enqueued: {request.feed_url}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
