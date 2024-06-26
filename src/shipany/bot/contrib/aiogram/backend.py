import asyncio
import logging

from shipany.bot.config import BotConfig
from shipany.bot.contrib.aiogram import router
from shipany.bot.contrib.aiogram.factories.telegram_objects import bot, dispatcher
from shipany.bot.conversation.models import Flow

logger = logging.getLogger(__name__)


async def serve(flow: Flow) -> None:
  bot_config = BotConfig()
  instance = bot()

  dp = dispatcher()
  dp.include_router(router.create(flow))

  if bot_config.telegram_webhook_url:
    return await asyncio.sleep(0)  # no op, because when webhook is set, the bot will be updated by the telegram server

  return await dp.start_polling(instance)
