import os
from dataclasses import dataclass


@dataclass
class Settings:
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key")
    smtp_server: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    imap_server: str = os.getenv("IMAP_SERVER", "imap.gmail.com")
    imap_port: int = int(os.getenv("IMAP_PORT", "993"))


settings = Settings()
