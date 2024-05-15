import pytest
from aiogram.types import TelegramObject

from shipany.bot.contrib.aiogram.actions.transition import GoToStep, process
from shipany.bot.contrib.aiogram.context import Context
from shipany.bot.conversation.v1.models.actions import TransitionAction


@pytest.mark.parametrize(
  ("action", "expected_step_id"),
  [
    (TransitionAction(**{"type": "transition", "next-step": "hello", "condition": None}), "hello"),
    (TransitionAction(**{"type": "transition", "next-step": "hello", "condition": {"==": [0, 0]}}), "hello"),
  ],
)
@pytest.mark.asyncio()
async def test_transition_action_to_next_step(action: TransitionAction, expected_step_id: str) -> None:
  ctx = Context(event=TelegramObject())
  result = await process(ctx, action)
  match result:
    case GoToStep(step_id=step_id):
      assert step_id == expected_step_id
    case _:  # pragma: no cover
      pytest.fail("Unexpected result")
