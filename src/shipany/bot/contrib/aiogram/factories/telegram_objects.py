from aiogram.client.bot import Bot

from shipany.bot.config import bot_config


def bot() -> Bot:
  return Bot(token=bot_config.token.get_secret_value())
