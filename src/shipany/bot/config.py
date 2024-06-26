from __future__ import annotations

from pydantic import Field, HttpUrl, SecretStr
from pydantic_settings import BaseSettings


class BotConfig(BaseSettings):
  token: SecretStr = Field(alias="BOT_TOKEN")
  telegram_api_url: str = Field(alias="TELEGRAM_API_URL", default="https://api.telegram.org")
  telegram_webhook_url: HttpUrl | None = Field(alias="TELEGRAM_WEBHOOK_URL", default=None)
  web_server_host: str = Field(alias="WEB_SERVER_HOST", default="127.0.0.1")
  web_server_port: int = Field(alias="WEB_SERVER_PORT", default=8000)
  web_bot_webhook_path: str = Field(alias="WEB_BOT_WEBHOOK_PATH", default="/bot-webhook")
  web_bot_webhook_secret: SecretStr = Field(alias="WEB_BOT_WEBHOOK_SECRET", default=SecretStr(""))
