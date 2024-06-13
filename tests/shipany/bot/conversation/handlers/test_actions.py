import pytest
from aiogram.types import TelegramObject
from pydantic import ValidationError

from shipany.bot.contrib.aiogram.context import bot_context
from shipany.bot.conversation.handlers.actions import handle
from shipany.bot.conversation.models.action import BaseAction


@pytest.mark.asyncio()
async def test_nonimportable_action() -> None:
  with pytest.raises(NotImplementedError, match="shipany.bot.actions.unknown_action.v1"), bot_context(
    TelegramObject()
  ) as ctx:
    await handle(BaseAction(name="UnknownAction@1"), ctx)


@pytest.mark.asyncio()
async def test_invalid_action_model() -> None:
  with pytest.raises(ValidationError), bot_context(TelegramObject()) as ctx:
    await handle(BaseAction.model_validate({"name": "StateAction@1", "unknown": "value"}), ctx)
