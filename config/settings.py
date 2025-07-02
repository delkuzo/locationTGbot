"""Configuration settings for the Location TG Bot."""

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Telegram Bot
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    webhook_url: str | None = os.getenv("WEBHOOK_URL", None)

    # OpenAI
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = "gpt-4o-mini"
    openai_max_tokens: int = 200
    openai_temperature: float = 1.0
    openai_timeout: int = 30  # seconds

    # Rate limiting
    rate_limit_requests: int = 1
    rate_limit_period: int = 5  # seconds

    # Application
    environment: str = os.getenv("ENVIRONMENT", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    # Server
    host: str = "0.0.0.0"
    port: int = int(os.getenv("PORT", "8000"))

    # System prompts
    system_prompt_ru: str = """Ты гид по местности. Пользователь отправляет тебе координаты.
Найди интересный, необычный или малоизвестный факт о любом месте в радиусе 500 метров от этих координат.
Ответь одним-двумя предложениями, не более 512 символов. Не используй markdown и ссылки."""

    system_prompt_en: str = """You are a local guide. The user sends you coordinates.
Find an interesting, unusual or little-known fact about any place within 500 meters of these coordinates.
Reply with one or two sentences, no more than 512 characters. Don't use markdown or links."""

    class Config:
        """Pydantic configuration."""

        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create global settings instance
settings = Settings()
