# Worker.py

# Imports
import asyncio
import json
import aio_pika
import uuid

from app.config.settings import settings
print("🐇 Connecting to RabbitMQ at:", settings.rabbitmq_url)

from app.services.email_service import send_email
from app.services.sms_service import send_sms
from app.services.push_service import send_push
from app.services.logger import log_notification
from app.utils.retry import retry
from app.queue.rabbitmq import send_to_dlq


QUEUE_NAME = "notifications"
DLQ_NAME = "notifications.dlq"

async def handle_message(message: aio_pika.IncomingMessage):
    """
    Handles incoming messages from RabbitMQ
    Determines notification type and routes accordingly.
    """
    async with message.process():   # Marks message as acknowledged once block finishes.

        try:
            payload = json.loads(message.body)
            notif_id = payload.get("id", str(uuid.uuid4()))

            print(f"[{notif_id}] 📬 Received a message from queue")
            
            notif_type = payload.get("type", "unknown")
            to = payload.get("to", "")
            subject = payload.get("subject", "")
            body = payload.get("body", "")

            # Route based on notification type
            if notif_type == "email":
                await retry(send_email, to, subject, body, notif_id=notif_id)
            elif notif_type == "sms":
                await retry(send_sms, to, body, notif_id=notif_id)
            elif notif_type == "push":
                await retry(send_push, to, body, notif_id=notif_id)
            else:
                print(f"Unknown notification type: {notif_type}")

            await log_notification(
                notif_id, notif_type, to, subject, body,
                status="success"
            )   

        except Exception as e:
            await log_notification(
                notif_id, 
                notif_type, 
                to, 
                subject, 
                body,
                status="failed",
                error=str(e)
            )
            await send_to_dlq(payload)
            print(f"[{notif_id}] 📦 Sent failed message to DLQ")

async def main():
    """
    Connects to RabbitMQ and starts consuming messages.
    """
    connection = await aio_pika.connect_robust(settings.rabbitmq_url)
    channel = await connection.channel()

    queue = await channel.declare_queue(QUEUE_NAME, durable=True)
    dlq = await channel.declare_queue(DLQ_NAME, durable=True)

    print(f"Worker started. Listening to queue: {QUEUE_NAME}")
    await queue.consume(handle_message)

    # Keep the worker running
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())