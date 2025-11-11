from fastapi import APIRouter
from utils.db import test_mongo_connection
from utils.mq import test_rabbitmq_connection

router = APIRouter()

@router.get("/")
def health_check():
    return {
        "mongo": test_mongo_connection(),
        "rabbitmq": test_rabbitmq_connection(),
        "status": "ok"
    }
