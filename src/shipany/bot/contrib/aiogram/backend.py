from typing import Any, Coroutine

from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.dispatcher.dispatcher import Dispatcher

from shipany.bot.config import BotConfig
from shipany.bot.conversation.models import Flow


def dispatcher(flow: Flow) -> Dispatcher:
  from shipany.bot.contrib.aiogram import router

  dp = Dispatcher()
  dp.include_router(router.create(flow))
  return dp


def create_instance(config: BotConfig) -> Bot:
  session = AiohttpSession(api=TelegramAPIServer.from_base(config.api_url))
  return Bot(config.token.get_secret_value(), session=session)


def serve(flow: Flow, bot_config: BotConfig) -> Coroutine[Any, Any, None]:
  instance = create_instance(bot_config)
  return dispatcher(flow).start_polling(instance)
