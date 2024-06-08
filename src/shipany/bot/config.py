from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class BotConfig(BaseSettings):
  token: SecretStr = Field(alias="BOT_TOKEN")
  api_url: str = Field(alias="TELEGRAM_API_URL", default="https://api.telegram.org")
  web_server_host: str = Field(alias="WEB_SERVER_HOST", default="127.0.0.1")
  web_server_port: int = Field(alias="WEB_SERVER_PORT", default=8000)


bot_config = BotConfig()
