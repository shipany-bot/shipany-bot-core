# mypy: disable-error-code="has-type"
from __future__ import annotations

import logging
import typing as t
from argparse import Namespace  # provides dot access to the attributes
from collections.abc import Mapping
from itertools import chain

from aiogram import types as aiogram_types
from aiogram.types.reaction_type_emoji import ReactionTypeEmoji

if t.TYPE_CHECKING:
  from shipany.bot.conversation.context import ConversationContext


logger = logging.getLogger(__name__)


def _fullfil_message_attribute(event: aiogram_types.Message) -> t.Any:  # noqa: ANN401
  match event:
    case aiogram_types.Message(message_id=message_id, text=text):
      return Namespace(id=message_id, text=text)
  t.assert_never(event)


def _fullfil_user_attribute(event: aiogram_types.Message | aiogram_types.MessageReactionUpdated) -> t.Any:  # noqa: ANN401
  match event:
    case aiogram_types.Message(from_user=aiogram_types.User(first_name=first_name, last_name=last_name, id=id)):
      return Namespace(id=id, first_name=first_name, last_name=last_name)
    case aiogram_types.MessageReactionUpdated(
      user=aiogram_types.User(first_name=first_name, last_name=last_name, id=id)
    ):
      return Namespace(id=id, first_name=first_name, last_name=last_name)
  t.assert_never(event)


def _fullfil_reaction_attribute(event: aiogram_types.MessageReactionUpdated) -> t.Any:  # noqa: ANN401
  match event:
    case aiogram_types.MessageReactionUpdated(new_reaction=new_reaction, old_reaction=old_reaction):
      return Namespace(
        new_reaction=[
          item.emoji if isinstance(item, ReactionTypeEmoji) else item.custom_emoji_id for item in new_reaction
        ],
        old_reaction=[
          item.emoji if isinstance(item, ReactionTypeEmoji) else item.custom_emoji_id for item in old_reaction
        ],
      )
  t.assert_never(event)


ProxyEventCallable = t.Callable[[aiogram_types.TelegramObject], t.Any]

ATTRIBUTES_MAPPING: t.Final[dict[str, ProxyEventCallable]] = {
  "message": _fullfil_message_attribute,
  "user": _fullfil_user_attribute,
  "reaction": _fullfil_reaction_attribute,
}


class VariablesGetter(Mapping[str, t.Any]):
  def __init__(self: t.Self, ctx: ConversationContext) -> None:
    self._ctx = ctx

  def __getitem__(self: t.Self, key: str) -> t.Any:  # noqa: ANN401
    logger.info("Getting the attribute: %s", key)

    if proxy := ATTRIBUTES_MAPPING.get(key):
      # restrict the access to curtain attributes
      return proxy(self._ctx.event)

    if key == "secrets":
      return self._ctx.runtime.secrets

    if key in self._ctx.captures:
      logger.info("Fetching %s from captures", key)
      return self._ctx.captures[key]

    raise KeyError(key)

  def __iter__(self: t.Self) -> t.Iterator[str]:
    return chain(iter(self._ctx.captures), iter(ATTRIBUTES_MAPPING.keys()))

  def __len__(self: t.Self) -> int:
    return len(self._ctx.captures) + len(ATTRIBUTES_MAPPING.keys())
