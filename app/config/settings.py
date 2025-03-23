# Config.py

# Imports
from pydantic import BaseSettings, EmailStr

# Settings Class
class Settings(BaseSettings):
    
    rabbitmq_url: str

    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_pass: str

    default_from: EmailStr

    class Config:
        env_file = ".env"


settings = Settings()
    