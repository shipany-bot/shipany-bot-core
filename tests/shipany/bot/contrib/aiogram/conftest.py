import datetime

import pytest
from aiogram.types import Message, MessageReactionUpdated, ReactionTypeEmoji, TelegramObject
from aiogram.types.chat import Chat
from aiogram.types.user import User


@pytest.fixture()
def private_chat_1() -> Chat:
  return Chat(id=1, type="private")


@pytest.fixture()
def user_1() -> User:
  return User(
    id=1,
    is_bot=False,
    first_name="John",
    last_name="Doe",
    username="johndoe",
  )


@pytest.fixture()
def hello_message(private_chat_1: Chat, user_1: User) -> Message:
  return Message(
    message_id=1,
    chat=private_chat_1,
    date=datetime.datetime.now(tz=datetime.timezone.utc),
    text="Hello",
    from_user=user_1,
  )


@pytest.fixture()
def hi_message(private_chat_1: Chat, user_1: User) -> Message:
  return Message(
    message_id=1,
    chat=private_chat_1,
    date=datetime.datetime.now(tz=datetime.timezone.utc),
    text="hi",
    from_user=user_1,
  )


@pytest.fixture()
def message_reaction_updated(private_chat_1: Chat, user_1: User) -> MessageReactionUpdated:
  return MessageReactionUpdated(
    message_id=1,
    chat=private_chat_1,
    date=datetime.datetime.now(tz=datetime.timezone.utc),
    new_reaction=[ReactionTypeEmoji(emoji="👍")],
    old_reaction=[],
    user=user_1,
  )


@pytest.fixture()
def telegram_event(request: pytest.FixtureRequest, telegram_event_fixture_name: str) -> TelegramObject:
  return request.getfixturevalue(telegram_event_fixture_name)
