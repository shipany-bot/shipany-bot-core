import pytest
from aiogram.types import TelegramObject

from shipany.bot import errors
from shipany.bot.contrib.aiogram.context import Context
from shipany.bot.contrib.aiogram.factories.send_message import construct_from
from shipany.bot.conversation.v1.models.actions import MessageAction


@pytest.mark.parametrize(
  "telegram_event_fixture_name",
  ["hello_message", "message_reaction_updated"],
)
@pytest.mark.parametrize(
  "action",
  [
    MessageAction(**{"type": "reply", "content": "Hello"}),
    MessageAction(**{"type": "answer", "content": "Hello"}),
  ],
)
def test_send_message_is_constructed(telegram_event: TelegramObject, action: MessageAction) -> None:
  method = construct_from(Context(event=telegram_event), action)
  assert method


def test_send_message_is_not_constructed() -> None:
  with pytest.raises(errors.NotImplementedError):
    construct_from(Context(event=TelegramObject()), MessageAction(**{"type": "reply", "content": "Hello"}))
