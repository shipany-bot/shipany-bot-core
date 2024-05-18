import pytest
from aiogram.types import TelegramObject

from shipany.bot.actions.transition_action.v1 import TransitionAction
from shipany.bot.contrib.aiogram.context import Context
from shipany.bot.contrib.aiogram.process.transition_action.v1 import GoToStep, process


@pytest.mark.parametrize(
  ("action", "expected_step_id"),
  [
    (
      TransitionAction(**{"name": "TransitionAction@1", "type": "transition", "next-step": "hello", "condition": None}),
      "hello",
    ),
    (
      TransitionAction(
        **{"name": "TransitionAction@1", "type": "transition", "next-step": "hello", "condition": {"==": [0, 0]}}
      ),
      "hello",
    ),
  ],
)
@pytest.mark.asyncio()
async def test_transition_action_to_next_step(action: TransitionAction, expected_step_id: str) -> None:
  ctx = Context(event=TelegramObject())
  result = process(ctx, action)
  match result:
    case GoToStep(step_id=step_id):
      assert step_id == expected_step_id
    case _:  # pragma: no cover
      pytest.fail("Unexpected result")
