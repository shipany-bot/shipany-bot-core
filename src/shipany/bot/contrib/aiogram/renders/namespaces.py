# mypy: disable-error-code="has-type"
from __future__ import annotations

import typing as t
from argparse import Namespace  # provides dot access to the attributes

from aiogram import types as aiogram_types
from aiogram.types.reaction_type_emoji import ReactionTypeEmoji

if t.TYPE_CHECKING:
  from shipany.bot.conversation.context import ConversationContext


def message_namespace(ctx: ConversationContext) -> Namespace | None:
  match ctx.event:
    case aiogram_types.Message(message_id=message_id, text=text):
      return Namespace(id=message_id, text=text)
  return None


def user_namespace(ctx: ConversationContext) -> Namespace | None:
  match ctx.event:
    case aiogram_types.Message(from_user=aiogram_types.User(first_name=first_name, last_name=last_name, id=id)):
      return Namespace(id=id, first_name=first_name, last_name=last_name)
    case aiogram_types.MessageReactionUpdated(
      user=aiogram_types.User(first_name=first_name, last_name=last_name, id=id)
    ):
      return Namespace(id=id, first_name=first_name, last_name=last_name)
  return None


def reaction_namespace(ctx: ConversationContext) -> Namespace | None:
  match ctx.event:
    case aiogram_types.MessageReactionUpdated(new_reaction=new_reaction, old_reaction=old_reaction):
      return Namespace(
        new_reaction=[
          item.emoji if isinstance(item, ReactionTypeEmoji) else item.custom_emoji_id for item in new_reaction
        ],
        old_reaction=[
          item.emoji if isinstance(item, ReactionTypeEmoji) else item.custom_emoji_id for item in old_reaction
        ],
      )
  return None
