import pika, json, os
from dotenv import load_dotenv

load_dotenv()
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "feeds_queue")

def publish_feed(feed_url):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    message = json.dumps({"feed_url": feed_url})
    channel.basic_publish(
        exchange='',
        routing_key=RABBITMQ_QUEUE,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()
    print(f"Published feed: {feed_url}")

def test_rabbitmq_connection():
    try:
        conn = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        conn.close()
        return "connected"
    except Exception as e:
        return f"error: {e}"
