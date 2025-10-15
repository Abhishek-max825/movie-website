import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Telegram Movie Streamer"
    environment: str = os.getenv("ENVIRONMENT", "development")

    # CORS
    cors_allow_origins: str = os.getenv("CORS_ALLOW_ORIGINS", "*")

    # Telethon (optional for compliant version)
    telegram_api_id: Optional[int] = None
    telegram_api_hash: Optional[str] = None
    telegram_bot_token: Optional[str] = None
    telegram_search_chats: Optional[str] = None  # comma-separated chat usernames/ids

    # Storage
    temp_dir: str = os.getenv("TEMP_DIR", "temp")
    hls_dirname: str = os.getenv("HLS_DIRNAME", "hls")
    cleanup_after_seconds: int = int(os.getenv("CLEANUP_AFTER_SECONDS", "3600"))

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()  # validate on import


