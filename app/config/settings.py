# Config.py

# Imports
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr

# Settings Class
class Settings(BaseSettings):
    
    rabbitmq_url: str
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"

    smtp_port: int = 587
    smtp_user: str = ""
    smtp_pass: str = ""
    default_from: EmailStr = "noreply@example.com"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"  # 👈 THIS allows extra keys in the .env
    )

settings = Settings()
