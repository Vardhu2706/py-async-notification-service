# Email Service

# Imports
import aiosmtplib
from email.message import EmailMessage
from app.config.settings import settings

async def send_email(to: str, subject: str, body: str):
    """
    Sends an email asynchronously using SMTP.

    Args:
        to (str): Recipient email address.
        subject (str): Subject line of the email.
        body (str): Plain text body content.

    Raises:
        aiosmtplib.SMTPException: If sending fails (caller handles retry).
    """

    # Create the email message
    message = EmailMessage()
    message["From"] = settings.default_from
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)

    # Send the email via SMTP (Mailtrap or other SMTP server)
    await aiosmtplib.send(
        message,
        hostname=settings.smtp_host,
        port=settings.smtp_port,
        username=settings.smtp_user,
        password=settings.smtp_pass,
        start_tls=True
    )

    print(f"[EMAIL] ✅ Sent to: {to} | Subject: {subject}")