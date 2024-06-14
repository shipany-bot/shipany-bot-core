import logging
import typing as t

from aiogram.methods import SendMessage
from aiogram.types import Message, MessageReactionUpdated

from shipany.bot import errors
from shipany.bot.actions.message_action.v1 import MessageAction, SupportedMessageActionTypes
from shipany.bot.conversation.context import ConversationContext
from shipany.bot.conversation.renders.jinja_env import template_from_context

logger = logging.getLogger(__name__)


def construct_from(ctx: ConversationContext, action: MessageAction) -> SendMessage:
  match ctx.event:
    case MessageReactionUpdated(chat=chat, _bot=_bot):
      if action.action_type != SupportedMessageActionTypes.answer:
        logger.error(f"Only `answer` is supported. Instead {action.action_type} was provided.")
      content = template_from_context(action.content, ctx, safe=False)
      return SendMessage(chat_id=chat.id, text=content).as_(_bot)
    case Message():
      content = template_from_context(action.content, ctx, safe=False)
      match action.action_type:
        case SupportedMessageActionTypes.reply:
          return ctx.event.reply(content)
        case SupportedMessageActionTypes.answer:
          return ctx.event.answer(content)
      t.assert_never(action.action_type)  # unreachable

  raise errors.NotImplementedError(f"Bot can't answer from event type: {type(ctx.event).__name__}")
