import pytest
from pydantic import ValidationError

from shipany.bot.conversation.handlers.actions import handle
from shipany.bot.conversation.models.action import BaseAction
from shipany.bot.runtime.context import Context


@pytest.mark.asyncio()
async def test_nonimportable_action() -> None:
  with pytest.raises(NotImplementedError, match="shipany.bot.actions.unknown_action.v1"):
    await handle(BaseAction(name="UnknownAction@1"), Context())


@pytest.mark.asyncio()
async def test_invalid_action_model() -> None:
  with pytest.raises(ValidationError):
    await handle(BaseAction.model_validate({"name": "StateAction@1", "unknown": "value"}), Context())
