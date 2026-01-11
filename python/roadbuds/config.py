# config.py
import logging

import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    # Secrets (from env vars only in production)
    database_url: str
    secret_key: str

    # Non-secrets (can come from .env or defaults)
    app_name: str = "roadbuds"
    debug: bool = False
    log_level: int = logging.INFO

    class Config:
        env_file = (".env", "dev.env")
        case_sensitive = False
