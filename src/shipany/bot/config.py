from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class BotConfig(BaseSettings):
  token: SecretStr = Field(alias="BOT_TOKEN")
  api_url: str = Field(alias="TELEGRAM_API_URL", default="https://api.telegram.org")


bot_config = BotConfig()
