from __future__ import annotations

import pytest

from shipany.bot.actions.state_action.v1 import StateAction
from shipany.bot.contrib.aiogram.process.state_action.v1 import process
from shipany.bot.conversation.context import conversation_context
from shipany.bot.conversation.handlers.actions import Continue


@pytest.mark.parametrize(
  ("action", "setup_locals", "captures_after"),
  [
    (
      StateAction.model_validate({"name": "StateAction@1", "type": "remove", "key": "hello"}),
      {"hello": "1"},
      {},
    ),
    (
      StateAction.model_validate({"name": "StateAction@1", "type": "remove", "key": "hello", "value": "1"}),
      {"hello": "1"},
      {},
    ),
    (
      StateAction.model_validate({"name": "StateAction@1", "type": "store", "key": "hello", "value": "1"}),
      {},
      {"hello": "1"},
    ),
    (
      StateAction.model_validate({"name": "StateAction@1", "type": "remove", "key": "hello"}),
      {},
      {},
    ),
    (
      StateAction.model_validate({"name": "StateAction@1", "type": "load", "key": "hello"}),
      {"hello": "1"},
      {"hello": "1"},
    ),
    (
      StateAction.model_validate({"name": "StateAction@1", "type": "load", "key": "hello", "value": "1"}),
      {"hello": "1"},
      {"hello": "1"},
    ),
    (
      StateAction.model_validate({"name": "StateAction@1", "type": "load", "key": "world"}),
      {"hello": "1"},
      {"hello": "1"},
    ),
  ],
)
async def test_state_action(action: StateAction, captures_after: dict[str, str]) -> None:
  async with conversation_context() as ctx:
    result = process(ctx, action)
    match result:
      case Continue():
        assert ctx.captures == captures_after
      case _:  # pragma: no cover
        pytest.fail("Unexpected result")
