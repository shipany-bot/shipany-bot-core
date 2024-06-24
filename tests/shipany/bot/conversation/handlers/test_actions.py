import pytest
from pydantic import ValidationError

from shipany.bot.conversation.context import conversation_context
from shipany.bot.conversation.handlers.actions import handle
from shipany.bot.conversation.models.action import BaseAction


async def test_nonimportable_action() -> None:
  with pytest.raises(NotImplementedError, match="shipany.bot.actions.unknown_action.v1"):
    async with conversation_context() as ctx:
      await handle(BaseAction(name="UnknownAction@1"), ctx)


async def test_invalid_action_model() -> None:
  with pytest.raises(ValidationError):
    async with conversation_context() as ctx:
      await handle(BaseAction.model_validate({"name": "StateAction@1", "unknown": "value"}), ctx)
