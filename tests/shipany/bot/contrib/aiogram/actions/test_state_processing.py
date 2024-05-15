from __future__ import annotations

import pytest
from aiogram.types import TelegramObject

from shipany.bot.contrib.aiogram.actions.state import GoToNextAction, process
from shipany.bot.contrib.aiogram.context import Context
from shipany.bot.conversation.v1.models.actions import StateAction


@pytest.mark.parametrize(
  ("action", "captures_before", "captures_after"),
  [
    (StateAction(**{"type": "store", "key": "hello", "value": None}), {"hello": "1"}, {}),
    (StateAction(**{"type": "store", "key": "hello", "value": "1"}), {}, {"hello": "1"}),
  ],
)
@pytest.mark.asyncio()
async def test_state_action(
  action: StateAction, captures_before: dict[str, str], captures_after: dict[str, str]
) -> None:
  ctx = Context(event=TelegramObject())
  result = await process(ctx, action)
  match result:
    case GoToNextAction():
      assert ctx.captures == captures_after
    case _:  # pragma: no cover
      pytest.fail("Unexpected result")
