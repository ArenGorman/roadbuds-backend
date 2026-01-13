# config.py
import os
import logging

import pydantic_settings
import dotenv

dotenv.load_dotenv("../dev.env")


class Settings(pydantic_settings.BaseSettings):
    # Secrets (from env vars only in production)
    database_url: str = os.getenv("DATABASE_URL")
    secret_key: str = os.getenv("SECRET_KEY")

    # Non-secrets (can come from .env or defaults)
    app_name: str = "roadbuds"
    debug: bool = False
    log_level: int = logging.INFO

    class Config:
        env_file = (".env", "dev.env")
        case_sensitive = False
