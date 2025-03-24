# Notify.py

# Imports
from fastapi import APIRouter, HTTPException
from app.models.schema import NotificationRequest
from app.queue.rabbitmq import publish_message

# Create a router for all notification-related endpoints
router = APIRouter()

@router.post("/")
async def send_notifications(payload: NotificationRequest):
    """
    Handles incoming POST /notify/ requests.

    Steps:
        1. Validate the incoming notifcation payload (already done via Pydantic model)
        2. Perform Email Validation
        3. Send the message to RabbitMQ via the publish_message function
        4. Return a success response if enqueued, or an error otherwise
    """
    try:
        # Basic check for email address format
        if payload.type == "email" and "@" not in payload.to:
            raise HTTPException(status_code=400, detail="Invalid email address")
        
        # Publish the validated notitication to the RabbitMQ queue
        await publish_message(payload.model_dump())

        # Return a success response
        return {
            "status": "queued",
            "message": "Notification sent to queue"
        }
    
    except Exception as e:

        # Handle and report any errors
        raise HTTPException(status_code=500, detail=str(e))