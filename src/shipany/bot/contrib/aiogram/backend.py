from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer

from shipany.bot.config import BotConfig


def create_instance(config: BotConfig) -> Bot:
  session = AiohttpSession(api=TelegramAPIServer.from_base(config.api_url))
  return Bot(config.token.get_secret_value(), session=session)
