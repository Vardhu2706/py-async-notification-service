# Logger

# Imports
from sqlmodel import Session
from app.models.log import NotificationLog
from app.main import engine

async def log_notification(
    id: str,
    notif_type: str,
    to: str,
    subject: str,
    body: str,
    status: str,
    error: str = None
):
    log_entry = NotificationLog(
        id=id,
        type=notif_type,
        to=to,
        subject=subject,
        body=body,
        status=status,
        error=error,
    )

    with Session(engine) as session:
        session.add(log_entry)
        session.commit()