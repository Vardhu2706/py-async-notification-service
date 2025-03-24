# Main.py

# Imports
from fastapi import FastAPI
from app.api import notify
from sqlmodel import SQLModel, create_engine
from app.models.log import NotificationLog

engine = create_engine("sqlite:///notifications.db")
app = FastAPI(title="Async Notification Service")

# Include routes
app.include_router(notify.router, prefix="/notify", tags=["Notifications"])

def init_db():
    SQLModel.metadata.create_all(engine)


init_db()