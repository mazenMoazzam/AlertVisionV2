import json
import pika
import os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "feeds_queue")

def publish_feed(feed_url):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()

        channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

        message = json.dumps({"feed_url": feed_url})
        channel.basic_publish(
            exchange='',
            routing_key=RABBITMQ_QUEUE,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2, 
            )
        )

        print(f"Published feed to queue: {feed_url}")
        connection.close()

    except Exception as e:
        print(f"Failed to publish feed: {e}")


def publish_all_from_file(feeds_file="feeds.json"):
    try:
        with open(feeds_file, "r") as f:
            data = json.load(f)

        feeds = data.get("feeds", [])
        print(f"Publishing {len(feeds)} feeds to queue...")

        for feed_url in feeds:
            publish_feed(feed_url)

        print("All feeds published successfully.")

    except FileNotFoundError:
        print(f"File not found: {feeds_file}")
    except json.JSONDecodeError:
        print(f"Invalid JSON in {feeds_file}")


if __name__ == "__main__":
    publish_all_from_file()
