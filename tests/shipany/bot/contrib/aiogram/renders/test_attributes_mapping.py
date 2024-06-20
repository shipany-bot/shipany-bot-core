from __future__ import annotations

import typing as t

import pytest

from shipany.bot.conversation.context import conversation_context
from shipany.bot.conversation.renders.attributes_mapping import VariablesGetter
from shipany.bot.conversation.renders.jinja_env import value_from_context

if t.TYPE_CHECKING:
  from aiogram.types import Message, TelegramObject


@pytest.mark.parametrize(
  "setup_locals",
  [{"test": "test"}],
)
def test_getter_behaves_like_mapping(hi_message: Message) -> None:
  with conversation_context(event=hi_message) as ctx:
    getter = VariablesGetter(ctx, captures_scopes=[], safe=True)
    assert getter["test"] == "test"
    assert "test" in getter
    with pytest.raises(KeyError):
      getter["not_found"]


def test_getter_returns_only_text_value(hello_message: Message) -> None:
  with conversation_context(event=hello_message) as ctx:
    getter = VariablesGetter(ctx, captures_scopes=[], safe=True)
    assert getter["message"].text == hello_message.text
    with pytest.raises(AttributeError, match="message_id"):
      assert getter["message"].message_id == hello_message.message_id


@pytest.mark.parametrize(
  "setup_secrets",
  [{"secr3t": "passw0rd"}],
)
def test_getter_returns_secrets(hello_message: Message) -> None:
  with conversation_context(event=hello_message) as ctx:
    getter = VariablesGetter(ctx, captures_scopes=[], safe=True)
    assert "secr3t" in getter["secrets"]
    assert getter["secrets"]["secr3t"] == "passw0rd"


@pytest.mark.parametrize(
  "setup_secrets",
  [{"secr3t": "passw0rd"}],
)
def test_getter_returns_secrets_when_unsafe(hello_message: Message) -> None:
  with conversation_context(event=hello_message) as ctx:
    getter = VariablesGetter(ctx, captures_scopes=[], safe=False)
    assert "secr3t" in getter["secrets"]
    assert getter["secrets"]["secr3t"] != "passw0rd"


@pytest.mark.parametrize(
  ("telegram_event_fixture_name", "attribute", "expected_result"),
  [
    ("hello_message", "message.text", "Hello"),
    ("hello_message", "message.id", "1"),
    ("hello_message", "user.id", "1"),
    ("message_reaction_updated", "user.id", "1"),
    ("message_reaction_updated", "user.first_name", "John"),
    ("message_reaction_updated", "reaction.new_reaction[0]", "👍"),
    ("message_reaction_updated", "reaction.old_reaction[0]", ""),
  ],
)
def test_getter_returns_user_attributes(telegram_event: TelegramObject, attribute: str, expected_result: str) -> None:
  with conversation_context(event=telegram_event) as ctx:
    assert value_from_context(attribute, ctx, scopes=[], safe=False) == expected_result
