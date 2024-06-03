from __future__ import annotations

import typing as t

import pytest
from aiogram.types import TelegramObject

from shipany.bot.actions.json_path_action.v1 import JsonPathAction
from shipany.bot.contrib.aiogram.context import Context
from shipany.bot.contrib.aiogram.process.json_path_action.v1 import Continue, process


@pytest.mark.parametrize(
  ("captures_before", "raw_action", "captures_after"),
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
async def test_state_action(
  captures_before: dict[str, str], raw_action: dict[str, t.Any], captures_after: dict[str, str]
) -> None:
  action = JsonPathAction(**raw_action)
  ctx = Context(captures=captures_before, event=TelegramObject())
  result = process(ctx, action)
  match result:
    case Continue():
      assert ctx.captures == captures_after
    case _:  # pragma: no cover
      pytest.fail("Unexpected result")
