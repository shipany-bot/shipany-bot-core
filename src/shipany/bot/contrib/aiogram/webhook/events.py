from __future__ import annotations

import logging
import typing as t

from shipany.bot.config import BotConfig
from shipany.bot.contrib.aiogram.factories.telegram_objects import bot, dispatcher

if t.TYPE_CHECKING:
  from pydantic import JsonValue

logger = logging.getLogger(__name__)


class WebserverEventsDispatcher:
  async def on_startup(self: t.Self) -> None:
    bot_config = BotConfig()

    info = await bot().get_webhook_info()
    if not bot_config.telegram_webhook_url:
      return

    if info.url and info.url != bot_config.telegram_webhook_url:
      ok = await bot().delete_webhook()
      if not ok:
        raise RuntimeError("Failed to delete the webhook")

    logger.info("Setting the webhook to %s", bot_config.telegram_webhook_url)

    ok = await bot().set_webhook(
      str(bot_config.telegram_webhook_url),
      secret_token=bot_config.web_bot_webhook_secret.get_secret_value(),
    )
    if not ok:
      raise RuntimeError("Failed to set the webhook")

  async def on_updates(self: t.Self, updates: dict[str, JsonValue]) -> t.Any:  # noqa: ANN401
    return await dispatcher().feed_raw_update(bot(), updates)

  async def on_shutdown(self: t.Self) -> None:
    ok = await bot().delete_webhook()
    if not ok:
      raise RuntimeError("Failed to delete the webhook")
