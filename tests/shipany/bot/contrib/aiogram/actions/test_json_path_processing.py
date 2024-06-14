from __future__ import annotations

import typing as t

import inject
import pytest
from aiogram.types import TelegramObject

from shipany.bot.actions.json_path_action.v1 import JsonPathAction
from shipany.bot.contrib.aiogram.context import bot_context
from shipany.bot.contrib.aiogram.process.json_path_action.v1 import process
from shipany.bot.conversation.handlers.actions import Continue, Terminate
from shipany.bot.providers.captures import CapturesProvider, InMemoryCapturesProvider

BinderCallable = t.Callable[[inject.Binder], None]


@pytest.fixture(autouse=True)
def captures_provider(setup_captures: t.Mapping[str, str]) -> BinderCallable:
  def _runtime_bindings(binder: inject.Binder) -> None:
    captures_provider = InMemoryCapturesProvider(initial_value=setup_captures)
    binder.bind(CapturesProvider, captures_provider)

  return _runtime_bindings


@pytest.mark.parametrize(
  ("setup_captures", "raw_action", "captures_after"),
  [
    (
      {"hello": '{"world": 1}'},
      {
        "name": "JsonPathAction@1",
        "expression": "$.world",
        "input": "{{hello}}",
        "captures": {"result": ""},
      },
      {"hello": '{"world": 1}', "result": "1"},
    ),
    (
      {"hello": '{"world": 1}'},
      {
        "name": "JsonPathAction@1",
        "expression": "$.world",
        "input": "{{hello}}",
        "captures": {},
      },
      {"hello": '{"world": 1}'},
    ),
    (
      {"hello": '[{"world": 1}, {"world": 2}]'},
      {
        "name": "JsonPathAction@1",
        "expression": "[*].world",
        "input": "{{hello}}",
        "captures": {"result1": "", "result2": ""},
      },
      {"hello": '[{"world": 1}, {"world": 2}]', "result1": "1", "result2": "2"},
    ),
    (
      {"hello": '[{"world": 1}, {"world": 2}]'},
      {
        "name": "JsonPathAction@1",
        "expression": "[*].world",
        "input": "{{hello}}",
        "captures": {"result1": ""},
      },
      {"hello": '[{"world": 1}, {"world": 2}]', "result1": "1"},
    ),
  ],
)
@pytest.mark.asyncio()
async def test_state_action(raw_action: dict[str, t.Any], captures_after: dict[str, str]) -> None:
  action = JsonPathAction(**raw_action)
  with bot_context(event=TelegramObject()) as ctx:
    result = process(ctx, action)
    match result:
      case Continue():
        assert ctx.captures == captures_after
      case _:  # pragma: no cover
        pytest.fail("Unexpected result")


@pytest.mark.parametrize(
  "setup_captures",
  [{}],
)
@pytest.mark.parametrize(
  "invalid_action",
  [
    {
      "name": "JsonPathAction@1",
      "expression": "$.world",
      "input": "invalid",
      "captures": {"result": ""},
    },
  ],
)
@pytest.mark.asyncio()
async def test_invalid_state_action(invalid_action: dict[str, t.Any]) -> None:
  action = JsonPathAction(**invalid_action)
  with bot_context(event=TelegramObject()) as ctx:
    result = process(ctx, action)
    assert isinstance(result, Terminate)
