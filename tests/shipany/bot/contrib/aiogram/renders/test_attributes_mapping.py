from __future__ import annotations

import typing as t

import pytest

from shipany.bot.contrib.aiogram.context import ExtendedContext
from shipany.bot.contrib.aiogram.renders import template_from_context
from shipany.bot.contrib.aiogram.renders.attributes_mapping import ATTRIBUTES_MAPPING, VariablesGetter

if t.TYPE_CHECKING:
  from aiogram.types import Message, TelegramObject


def test_getter_behaves_like_mapping(hello_message: Message) -> None:
  ctx = VariablesGetter(ExtendedContext(event=hello_message, captures={"test": "test"}))
  assert ctx["test"] == "test"
  assert "test" in ctx
  assert len(ctx) == len(ATTRIBUTES_MAPPING) + 1
  assert list(ctx) == ["test", *ATTRIBUTES_MAPPING.keys()]
  with pytest.raises(KeyError):
    ctx["not_found"]


def test_getter_returns_only_text_value(hello_message: Message) -> None:
  ctx = VariablesGetter(ExtendedContext(event=hello_message))
  assert ctx["message"].text == hello_message.text
  with pytest.raises(AttributeError, match="message_id"):
    assert ctx["message"].message_id == hello_message.message_id


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
  ctx = ExtendedContext(event=telegram_event)
  assert template_from_context("{{" + attribute + "}}", ctx) == expected_result
