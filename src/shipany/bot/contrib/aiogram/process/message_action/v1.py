from shipany.bot.actions.message_action.v1 import MessageAction
from shipany.bot.contrib.aiogram.factories.send_message import construct_from as construct_message_from
from shipany.bot.conversation.context import ConversationContext
from shipany.bot.conversation.handlers.actions import AwaitObjectAndContinue


def process(ctx: ConversationContext, action: MessageAction) -> AwaitObjectAndContinue:
  return AwaitObjectAndContinue(value=construct_message_from(ctx, action))
