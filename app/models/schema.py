# Schema.py - Notification Payload Model

# Imports
from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import Optional

class NotificationType(str, Enum):

    email = "email"
    sms = "sms"
    push = "push"

class NotificationRequest(BaseModel):

    type: NotificationType
    to: str
    subject: Optional[str] = None
    body: str

