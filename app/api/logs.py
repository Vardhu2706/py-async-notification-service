# Logs.py

# Imports
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from app.models.log import NotificationLog
from app.db.session import engine

router = APIRouter()

@router.get("/{notif_id}")
def get_log_by_id(notif_id: str):
    """
    Fetches a log entry by notification ID.
    """
    with Session(engine) as session:
        statement = select(NotificationLog).where(NotificationLog.id == notif_id)
        result = session.exec(statement).first()

        if not result:
            raise HTTPException(status_code=404, detail="Notification log not found")
        
        return result