from shipany.bot.actions.message_action.v1 import MessageAction
from shipany.bot.contrib.aiogram.action_dispatcher import AwaitMethodAndContinue
from shipany.bot.contrib.aiogram.context import Context
from shipany.bot.contrib.aiogram.factories.send_message import construct_from as construct_message_from


def process(ctx: Context, action: MessageAction) -> AwaitMethodAndContinue:
  return AwaitMethodAndContinue(value=construct_message_from(ctx, action))
