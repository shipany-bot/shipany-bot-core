import logging
import typing as t

from shipany.bot.actions.state_action.v1 import StateAction, SupportedStateActionTypes
from shipany.bot.contrib.aiogram.action_dispatcher import Continue
from shipany.bot.contrib.aiogram.context import Context
from shipany.bot.contrib.aiogram.renders.jinja_env import template_from_context

logger = logging.getLogger(__name__)


def process(ctx: Context, action: StateAction) -> Continue:
  action_type = SupportedStateActionTypes(action.action_type)
  match action_type:
    case SupportedStateActionTypes.store:
      if action.value is None:
        ctx.captures.pop(action.key, None)
        logger.info(f"Removed key '{action.key}'")
      else:
        ctx.captures[action.key] = template_from_context(action.value, ctx)
        logger.info(f"Stored value '{ctx.captures[action.key]}' in key '{action.key}'")
      return Continue()
  t.assert_never(action_type)
