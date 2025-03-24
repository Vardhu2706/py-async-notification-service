# Log Model

# Imports 
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
import uuid

class NotificationLog(SQLModel, table=True):

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    type: str
    to: str
    subject: Optional[str] = None
    body: str
    status: str
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))