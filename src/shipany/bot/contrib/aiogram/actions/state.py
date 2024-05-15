import logging
import typing_extensions as t

from shipany.bot.contrib.aiogram.action_dispatcher import GoToNextAction
from shipany.bot.contrib.aiogram.context import Context
from shipany.bot.contrib.aiogram.renders.jinja_env import template_from_context
from shipany.bot.conversation.v1.models.actions.state import StateAction, SupportedStateActionTypes

logger = logging.getLogger(__name__)


async def process(ctx: Context, action: StateAction) -> GoToNextAction:
  action_type = SupportedStateActionTypes(action.action_type)
  match action_type:
    case SupportedStateActionTypes.store:
      if action.value is None:
        ctx.captures.pop(action.key, None)
        logger.info(f"Removed key '{action.key}'")
      else:
        ctx.captures[action.key] = template_from_context(action.value, ctx)
        logger.info(f"Stored value '{ctx.captures[action.key]}' in key '{action.key}'")
      return GoToNextAction()
  t.assert_never(action_type)
