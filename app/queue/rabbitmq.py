# RabbitMQ.py - Message Publisher

# Imports
import aio_pika
import json
from app.config.settings import settings

async def publish_message(message: dict, queue_name: str = "notifications"):
    """
    Publishes a message to the specified RabbitMQ queue ising aio-pika

    Args:
        message (dict): The message payload to be sent (e.g., notification details)
        queue_name (str): The name of the RabbitMQ queue to publish to. Default is "notifications".
    
    Steps:
        1. Connect to RabbitMQ using connection URL from .env
        2. Open a channel (like a lightweight TCP stream within connection)
        3. Publish the message (as JSON) to the default exchange using the queue name as routing key
    """

    #  Estblish a robust connection to RabbitMQ (auto-reconnect on failure)
    connection = await aio_pika.connect_robust(settings.rabbitmq_url)

    # Automatically close connection after this block
    async with connection:

        # Open a channel
        channel = await connection.channel()

        # Serialize message as JSON and publish to default exchange
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(message).encode()),    # Message body must be bytes
            routing_key=queue_name                                  # Determines which queue the messags goes to
        )


# Sends a failed notification payload to the Dead Letter Queue (DLQ)
async def send_to_dlq(payload: dict):

    # Establish a connection to RabbitMQ using the configured URL
    connection = await aio_pika.connect_robust(settings.rabbitmq_url)

    # Open a channel to publish the message
    channel = await connection.channel()

    # Publish the payload to the 'notifications.dlq' queue using the default exchange
    await channel.default_exchange.publish(
        aio_pika.Message(body=json.dumps(payload).encode()),     # Serialize & encode the message
        routing_key="notifications.dlq"
    )

    # Log confirmation
    print("📦 Message sent to DLQ")