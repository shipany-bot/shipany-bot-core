import logging
import typing as t

from shipany.bot.actions.state_action.v1 import StateAction, SupportedStateActionTypes
from shipany.bot.conversation.context import ConversationContext
from shipany.bot.conversation.handlers.actions import Continue
from shipany.bot.conversation.renders.jinja_env import template_from_context

logger = logging.getLogger("StateAction@v1")


def process(ctx: ConversationContext, action: StateAction) -> Continue:
  match action.action_type:
    case SupportedStateActionTypes.store:
      if action.value is not None:
        ctx.captures.set(action.key, template_from_context(action.value, ctx, safe=True), scope=[])

    case SupportedStateActionTypes.remove:
      if action.value is not None:
        logger.warning(f"Value '{action.value}' is ignored for 'remove' action type.")
      try:
        ctx.captures.remove(action.key, scope=[])
      except KeyError:
        logger.warning(f"Key '{action.key}' doesn't exist.")

    case _:
      t.assert_never(action.action_type)
  return Continue()
