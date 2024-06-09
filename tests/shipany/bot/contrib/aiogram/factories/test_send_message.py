import pytest
from aiogram.types import TelegramObject

from shipany.bot import errors
from shipany.bot.actions.message_action.v1 import MessageAction
from shipany.bot.contrib.aiogram.context import ExtendedContext as Context
from shipany.bot.contrib.aiogram.factories.send_message import construct_from


@pytest.mark.parametrize(
  "telegram_event_fixture_name",
  ["hello_message", "message_reaction_updated"],
)
@pytest.mark.parametrize(
  "action",
  [
    MessageAction(**{"name": "MessageAction@1", "type": "reply", "content": "Hello"}),
    MessageAction(**{"name": "MessageAction@1", "type": "answer", "content": "Hello"}),
  ],
)
def test_send_message_is_constructed(telegram_event: TelegramObject, action: MessageAction) -> None:
  method = construct_from(Context(event=telegram_event), action)
  assert method


def test_send_message_is_not_constructed() -> None:
  with pytest.raises(errors.NotImplementedError):
    construct_from(
      Context(event=TelegramObject()), MessageAction(**{"name": "MessageAction@1", "type": "reply", "content": "Hello"})
    )
