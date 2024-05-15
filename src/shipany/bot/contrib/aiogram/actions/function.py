import logging

from shipany.bot.contrib.aiogram.action_dispatcher import GoToNextAction
from shipany.bot.contrib.aiogram.context import Context
from shipany.bot.conversation.v1.models.actions.function import FunctionAction

logger = logging.getLogger(__name__)


async def process(ctx: Context, action: FunctionAction) -> GoToNextAction:
  logger.info("Executing function: %s", action.call)
  return GoToNextAction()
