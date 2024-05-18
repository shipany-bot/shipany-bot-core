from shipany.bot.actions.message_action.v1 import MessageAction
from shipany.bot.contrib.aiogram.action_dispatcher import ReturnValue
from shipany.bot.contrib.aiogram.context import Context
from shipany.bot.contrib.aiogram.factories.send_message import construct_from as construct_message_from


def process(ctx: Context, action: MessageAction) -> ReturnValue:
  return ReturnValue(value=construct_message_from(ctx, action))
