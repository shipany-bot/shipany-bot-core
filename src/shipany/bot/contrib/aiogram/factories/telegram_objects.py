from functools import lru_cache

from aiogram.client.bot import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.dispatcher.dispatcher import Dispatcher

from shipany.bot.config import BotConfig


@lru_cache
def bot() -> Bot:  # pragma: no cover
  bot_config = BotConfig()
  session = AiohttpSession(api=TelegramAPIServer.from_base(bot_config.telegram_api_url))
  return Bot(bot_config.token.get_secret_value(), session=session)


@lru_cache
def dispatcher() -> Dispatcher:
  return Dispatcher()
