# Worker.py

# Imports
import asyncio
import json
import aio_pika

from app.config.settings import settings
from app.services.email_service import send_email
from app.services.sms_service import send_sms
from app.services.push_service import send_push

QUEUE_NAME = "notifications"

async def handle_message(message: aio_pika.IncomingMessage):
    """
    Handles incoming messages from RabbitMQ
    Determines notification type and routes accordingly.
    """
    async with message.process():   # Marks message as acknowledged once block finishes.
        try:
            payload = json.loads(message.body)

            notif_type = payload.get("type")
            to = payload.get("to")
            subject = payload.get("subject")
            body = payload.get("body")

            # Route based on notification type
            if notif_type == "email":
                await send_email(to, subject, body)
            elif notif_type == "sms":
                await send_sms(to, body)
            elif notif_type == "push":
                await send_push(to, body)
            else:
                print(f"Unknown notification type: {notif_type}")

        except Exception as e:
            print(f"Error processing message: {e}")


async def main():
    """
    Connects to RabbitMQ and starts consuming messages.
    """
    connection = await aio_pika.connect_robust(settings.rabbitmq_url)
    channel = await connection.channel()
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)

    print(f"Worker started, listening to queue: {QUEUE_NAME}")

    # Keep the worker running
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())