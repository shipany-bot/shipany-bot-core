import pytest
from aiogram.types import TelegramObject
from pydantic import ValidationError

from shipany.bot.conversation.context import conversation_context
from shipany.bot.conversation.handlers.actions import handle
from shipany.bot.conversation.models.action import BaseAction


@pytest.mark.asyncio()
async def test_nonimportable_action() -> None:
  with pytest.raises(NotImplementedError, match="shipany.bot.actions.unknown_action.v1"), conversation_context(
    TelegramObject()
  ) as ctx:
    await handle(BaseAction(name="UnknownAction@1"), ctx)


@pytest.mark.asyncio()
async def test_invalid_action_model() -> None:
  with pytest.raises(ValidationError), conversation_context(TelegramObject()) as ctx:
    await handle(BaseAction.model_validate({"name": "StateAction@1", "unknown": "value"}), ctx)
