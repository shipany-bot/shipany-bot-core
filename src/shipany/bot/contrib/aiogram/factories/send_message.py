import logging
from typing_extensions import assert_never

from aiogram.methods import SendMessage
from aiogram.types import Message, MessageReactionUpdated

from shipany.bot import errors
from shipany.bot.contrib.aiogram import renders
from shipany.bot.contrib.aiogram.context import Context
from shipany.bot.conversation.v1.models.actions import MessageAction, SupportedMessageActionTypes

logger = logging.getLogger(__name__)


def construct_from(ctx: Context, action: MessageAction) -> SendMessage:
  match ctx.event:
    case MessageReactionUpdated(chat=chat, _bot=_bot):
      if action.action_type != "answer":
        logger.error(f"Only `answer` is supported. Instead {action.action_type} was provided.")
      content = renders.template_from_context(action.content, ctx)
      return SendMessage(chat_id=chat.id, text=content).as_(_bot)
    case Message():
      action_type = SupportedMessageActionTypes(action.action_type)
      content = renders.template_from_context(action.content, ctx)
      match action_type:
        case SupportedMessageActionTypes.reply:
          return ctx.event.reply(content)
        case SupportedMessageActionTypes.answer:
          return ctx.event.answer(content)
      assert_never(action_type)  # unreachable

  raise errors.NotImplementedError(f"Bot can't answer from event type: {type(ctx.event)}")
