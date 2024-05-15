from __future__ import annotations

import logging
import typing as t
from typing_extensions import Self

from shipany.bot.contrib.aiogram.action_dispatcher import (
  DispatchedResult,
  GoToNextAction,
  GoToStep,
  ReturnValue,
  handle,
)
from shipany.bot.conversation.v1.handlers import EventHandler

if t.TYPE_CHECKING:
  from aiogram.methods import TelegramMethod

  from shipany.bot.contrib.aiogram.context import Context

logger = logging.getLogger(__name__)


class AiogramEventHandler(EventHandler):
  async def __call__(self: Self, context: Context) -> TelegramMethod | None:
    logger.info("Event handler called")
    actions = self.traverse_actions()
    for action in actions:
      logger.info("Executing action: %s", action)
      if not action:
        continue
      try:
        result: DispatchedResult = await handle(action, context)
      except (ImportError, NotImplementedError):
        logger.error("Error while processing action", exc_info=True)
        break

      match result:
        case ReturnValue(value=value):
          return value
        case GoToNextAction():
          continue
        case GoToStep(step_id=step_id):
          logger.info("Transitioning to next step: %s", step_id)
          actions.send(step_id)
    return None
