# Config.py

# Imports
import os
os.environ.pop("RABBITMQ_URL", None)

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr

# Settings Class
class Settings(BaseSettings):
    
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"

    smtp_host: str = "sandbox.smtp.mailtrap.io"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_pass: str = ""
    default_from: EmailStr = "noreply@example.com"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",          
        case_sensitive=False,   
        extra="allow"
    )


settings = Settings()

print("✅ Loaded RabbitMQ URL:", settings.rabbitmq_url)
