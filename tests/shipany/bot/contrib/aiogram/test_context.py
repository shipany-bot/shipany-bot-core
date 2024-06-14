from __future__ import annotations

import inject
import pytest
from aiogram.types import TelegramObject

from shipany.bot.actions.state_action.v1 import StateAction
from shipany.bot.contrib.aiogram.context import bot_context
from shipany.bot.contrib.aiogram.process.state_action.v1 import process
from shipany.bot.providers.captures import CapturesProvider


@pytest.mark.asyncio()
async def test_context_changes() -> None:
  action = StateAction.model_validate({"name": "StateAction@1", "type": "store", "key": "hello", "value": "1"})
  with bot_context(event=TelegramObject()) as ctx:
    process(ctx, action)

  provider: CapturesProvider = inject.instance(CapturesProvider)
  with provider.snapshot() as captures:
    assert captures == {"hello": "1"}
