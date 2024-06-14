import logging
import typing as t

from shipany.bot.actions.state_action.v1 import StateAction, SupportedStateActionTypes
from shipany.bot.conversation.context import ConversationContext
from shipany.bot.conversation.handlers.actions import Continue
from shipany.bot.conversation.renders.jinja_env import template_from_context

logger = logging.getLogger(__name__)


def process(ctx: ConversationContext, action: StateAction) -> Continue:
  action_type = SupportedStateActionTypes(action.action_type)
  match action_type:
    case SupportedStateActionTypes.store:
      if action.value is None:
        del ctx.captures[action.key]
        logger.info(f"Removed key '{action.key}'")
      else:
        ctx.captures[action.key] = template_from_context(action.value, ctx, safe=True)
        logger.info(f"Stored value '{ctx.captures[action.key]}' in key '{action.key}'")
      return Continue()
  t.assert_never(action_type)
