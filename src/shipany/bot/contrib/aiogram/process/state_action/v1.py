import logging
import typing as t

from shipany.bot.actions.state_action.v1 import StateAction, SupportedStateActionTypes
from shipany.bot.conversation.context import ConversationContext
from shipany.bot.conversation.handlers.actions import Continue
from shipany.bot.conversation.renders.jinja_env import template_from_context

logger = logging.getLogger("StateAction@v1")


def _update_captures(ctx: ConversationContext, action: StateAction) -> None:
  if action.value is not None:
    rendered_value = template_from_context(action.value, ctx, scopes=[], safe=True)
    ctx.captures.set(action.key, rendered_value, scope=action.scope)


def _remove_captures(ctx: ConversationContext, action: StateAction) -> None:
  if action.value is not None:
    logger.warning(f"Value '{action.value}' is ignored for 'remove' action type.")
  try:
    ctx.captures.remove(action.key, scope=action.scope)
  except KeyError:
    logger.warning(f"Key '{action.key}' doesn't exist.")


def _load_captures(ctx: ConversationContext, action: StateAction) -> None:
  if action.value is not None:
    logger.warning(f"Value '{action.value}' is ignored for 'load' action type.")
  try:
    value = ctx.captures.get(action.key, scope=action.scope)
    if value is not None:
      ctx.captures.set(action.key, value, scope=[])
  except KeyError:
    logger.warning(f"Key '{action.key}' doesn't exist.")


def process(ctx: ConversationContext, action: StateAction) -> Continue:
  match action.action_type:
    case SupportedStateActionTypes.store:
      _update_captures(ctx, action)

    case SupportedStateActionTypes.remove:
      _remove_captures(ctx, action)

    case SupportedStateActionTypes.load:
      _load_captures(ctx, action)

    case _:
      t.assert_never(action.action_type)
  return Continue()
