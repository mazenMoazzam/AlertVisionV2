import pika
import json
import os
import time
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
from pika.exceptions import AMQPConnectionError
from utils.detector import detect_objects

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "feeds_queue")
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB", "alertvision")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

def connect_with_retry(max_retries=10, delay=5):
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Attempting RabbitMQ connection ({attempt}/{max_retries})...")
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            print("Connected to RabbitMQ")
            return connection
        except AMQPConnectionError as e:
            print(f"RabbitMQ not ready yet ({e}). Retrying in {delay}s...")
            time.sleep(delay)
    raise Exception("Could not connect to RabbitMQ after several attempts.")

def process_feed(feed_url, mode="object"):
    print(f"Starting detection for feed: {feed_url}")
    try:
        events = detect_objects(feed_url, max_duration=15, mode=mode)
        result = {
            "feed_url": feed_url,
            "timestamp": datetime.utcnow(),
            "events": events,
            "status": "completed" if events else "no_detections"
        }
        db["detections"].insert_one(result)
        print(f"Stored {len(events)} events for {feed_url}")
    except Exception as e:
        print(f"Error processing {feed_url}: {e}")
        db["detections"].insert_one({
            "feed_url": feed_url,
            "timestamp": datetime.utcnow(),
            "status": "failed",
            "error": str(e)
        })


def callback(ch, method, properties, body):
    data = json.loads(body)
    feed_url = data.get("feed_url")
    if not feed_url:
        print("Received invalid message:", data)
        return

    print(f"Received feed from queue: {feed_url}")
    process_feed(feed_url)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"Finished processing feed: {feed_url}\n")


def start_worker():
    print("Worker started. Waiting for feeds...")
    connection = connect_with_retry()  
    channel = connection.channel()

    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback)

    print("Worker connected and listening for messages...")
    channel.start_consuming()


if __name__ == "__main__":
    start_worker()
