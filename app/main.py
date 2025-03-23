# Main.py

# Imports
from fastapi import FastAPI
from app.api import notify

app = FastAPI(title="Async Notification Service")

# Include routes
app.include_router(notify.router, prefix="/notify", tags=["Notifications"])