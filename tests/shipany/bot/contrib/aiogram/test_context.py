from __future__ import annotations

from shipany.bot.actions.state_action.v1 import StateAction
from shipany.bot.contrib.aiogram.process.state_action.v1 import process
from shipany.bot.conversation.context import conversation_context


async def test_context_changes() -> None:
  action = StateAction.model_validate({"name": "StateAction@1", "type": "store", "key": "hello", "value": "1"})
  async with conversation_context() as ctx:
    process(ctx, action)

  async with conversation_context() as ctx:
    assert ctx.captures == {"hello": "1"}
