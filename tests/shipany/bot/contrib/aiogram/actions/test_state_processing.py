from __future__ import annotations

import typing as t

import inject
import pytest
from aiogram.types import TelegramObject

from shipany.bot.actions.state_action.v1 import StateAction
from shipany.bot.contrib.aiogram.context import bot_context
from shipany.bot.contrib.aiogram.process.state_action.v1 import process
from shipany.bot.conversation.handlers.actions import Continue
from shipany.bot.providers.captures import CapturesProvider, InMemoryCapturesProvider

BinderCallable = t.Callable[[inject.Binder], None]


@pytest.fixture(autouse=True)
def captures_provider(setup_captures: t.Mapping[str, str]) -> BinderCallable:
  def _runtime_bindings(binder: inject.Binder) -> None:
    captures_provider = InMemoryCapturesProvider(initial_value=setup_captures)
    binder.bind(CapturesProvider, captures_provider)

  return _runtime_bindings


@pytest.mark.parametrize(
  ("action", "setup_captures", "captures_after"),
  [
    (
      StateAction.model_validate({"name": "StateAction@1", "type": "store", "key": "hello", "value": None}),
      {"hello": "1"},
      {},
    ),
    (
      StateAction.model_validate({"name": "StateAction@1", "type": "store", "key": "hello", "value": "1"}),
      {},
      {"hello": "1"},
    ),
  ],
)
@pytest.mark.asyncio()
async def test_state_action(action: StateAction, captures_after: dict[str, str]) -> None:
  with bot_context(event=TelegramObject()) as ctx:
    result = process(ctx, action)
    match result:
      case Continue():
        assert ctx.captures == captures_after
      case _:  # pragma: no cover
        pytest.fail("Unexpected result")
