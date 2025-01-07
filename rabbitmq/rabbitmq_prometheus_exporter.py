import os
import time
import requests
from prometheus_client import start_http_server, Gauge

# Environment variables
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")
PORT = int(os.getenv("PORT", 8000))
INTERVAL = int(os.getenv("INTERVAL", 10))  # Scrape interval in seconds

# Prometheus metrics
g_messages = Gauge(
    "rabbitmq_individual_queue_messages",
    "Total count of messages in RabbitMQ queue",
    ["host", "vhost", "name"]
)
g_messages_ready = Gauge(
    "rabbitmq_individual_queue_messages_ready",
    "Count of ready messages in RabbitMQ queue",
    ["host", "vhost", "name"]
)
g_messages_unacknowledged = Gauge(
    "rabbitmq_individual_queue_messages_unacknowledged",
    "Count of unacknowledged messages in RabbitMQ queue",
    ["host", "vhost", "name"]
)


def fetch_queue_metrics():
    url = f"http://{RABBITMQ_HOST}:15672/api/queues"
    try:
        response = requests.get(url, auth=(RABBITMQ_USER, RABBITMQ_PASSWORD))
        response.raise_for_status()
        queues = response.json()

        for queue in queues:
            vhost = queue.get("vhost", "unknown")
            name = queue.get("name", "unknown")
            messages = queue.get("messages", 0)
            messages_ready = queue.get("messages_ready", 0)
            messages_unacknowledged = queue.get("messages_unacknowledged", 0)

            # Set metrics
            g_messages.labels(RABBITMQ_HOST, vhost, name).set(messages)
            g_messages_ready.labels(RABBITMQ_HOST, vhost, name).set(messages_ready)
            g_messages_unacknowledged.labels(RABBITMQ_HOST, vhost, name).set(messages_unacknowledged)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching metrics: {e}")


def main():
    # Start Prometheus server
    start_http_server(PORT)
    print(f"Prometheus exporter started on port {PORT}")

    while True:
        fetch_queue_metrics()
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
