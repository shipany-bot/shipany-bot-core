from __future__ import annotations

import pytest
from aiogram import types

from shipany.bot.contrib.aiogram.persistency.handles import AiogramHandleGenerator, HandleGeneratorFactory
from shipany.bot.providers.captures import Scope


def test_handle_generator_with_none_will_fail() -> None:
  with pytest.raises(TypeError, match="Expected TelegramObject"):
    AiogramHandleGenerator(None)


@pytest.mark.parametrize(
  ("telegram_event_fixture_name", "scope", "expected"),
  [
    ("hello_message", [Scope.user], "1:_:key"),
    ("hello_message", [Scope.chat], "_:1:key"),
    ("hello_message", [Scope.user, Scope.chat], "1:1:key"),
    ("message_reaction_updated", [Scope.user], "1:_:key"),
    ("message_reaction_updated", [Scope.chat], "_:1:key"),
    ("message_reaction_updated", [Scope.user, Scope.chat], "1:1:key"),
  ],
)
def test_handle_generator_with_aiogram_types(
  telegram_event: types.TelegramObject, scope: list[Scope], expected: str
) -> None:
  handle_generator = AiogramHandleGenerator(telegram_event)
  assert handle_generator.generate("key", scope) == expected


def test_handle_generator_can_be_created() -> None:
  handle_generator = HandleGeneratorFactory().create(types.TelegramObject())
  assert handle_generator is not None
