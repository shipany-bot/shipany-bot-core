from __future__ import annotations

import pytest
from aiogram.types import TelegramObject

from shipany.bot.actions.state_action.v1 import StateAction
from shipany.bot.contrib.aiogram.context import Context
from shipany.bot.contrib.aiogram.process.state_action.v1 import Continue, process


@pytest.mark.parametrize(
  ("action", "captures_before", "captures_after"),
  [
    (StateAction(**{"name": "StateAction@1", "type": "store", "key": "hello", "value": None}), {"hello": "1"}, {}),
    (StateAction(**{"name": "StateAction@1", "type": "store", "key": "hello", "value": "1"}), {}, {"hello": "1"}),
  ],
)
@pytest.mark.asyncio()
async def test_state_action(
  action: StateAction, captures_before: dict[str, str], captures_after: dict[str, str]
) -> None:
  ctx = Context(captures=captures_before, event=TelegramObject())
  result = process(ctx, action)
  match result:
    case Continue():
      assert ctx.captures == captures_after
    case _:  # pragma: no cover
      pytest.fail("Unexpected result")
