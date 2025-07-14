import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    # === BASE / AUTH ===
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 43200
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    OAUTH2_TOKEN_URL: str = "/api/v1/auth/login"

    # === GENERAL SETTINGS ===
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    ALLOWED_HOSTS: list[str] = os.getenv("ALLOWED_HOSTS", "").split(",")

    # === DATABASE ===
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # === STORAGE ===
    