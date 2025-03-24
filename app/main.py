# Main.py

# Imports
from fastapi import FastAPI
from app.api import notify
from sqlmodel import SQLModel
from app.models.log import NotificationLog
from app.api import logs
from app.db.session import engine

app = FastAPI(title="Async Notification Service")

# Include routes
app.include_router(notify.router, prefix="/notify", tags=["Notifications"])
app.include_router(logs.router, prefix="/logs", tags=["Logs"])

def init_db():
    SQLModel.metadata.create_all(engine)

init_db()