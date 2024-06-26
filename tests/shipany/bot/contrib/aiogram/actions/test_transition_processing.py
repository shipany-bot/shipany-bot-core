import pytest

from shipany.bot.actions.transition_action.v1 import TransitionAction
from shipany.bot.contrib.aiogram.process.transition_action.v1 import process
from shipany.bot.conversation.context import conversation_context
from shipany.bot.conversation.handlers.actions import Continue, GoToStep


@pytest.mark.parametrize(
  ("action", "expected_step_id"),
  [
    (
      TransitionAction.model_validate({"name": "TransitionAction@1", "next-step": "hello", "condition": None}),
      "hello",
    ),
    (
      TransitionAction.model_validate(
        {"name": "TransitionAction@1", "next-step": "hello", "condition": {"==": [0, 0]}}
      ),
      "hello",
    ),
  ],
)
async def test_transition_action_to_next_step(action: TransitionAction, expected_step_id: str) -> None:
  async with conversation_context() as ctx:
    result = process(ctx, action)
    match result:
      case GoToStep(step_id=step_id):
        assert step_id == expected_step_id
      case _:  # pragma: no cover
        pytest.fail("Unexpected result")


@pytest.mark.parametrize(
  "action",
  [
    TransitionAction.model_validate({"name": "TransitionAction@1", "next-step": "hello", "condition": {"==": [0, 1]}}),
  ],
)
async def test_no_transition_action_to_next_step(action: TransitionAction) -> None:
  async with conversation_context() as ctx:
    result = process(ctx, action)
    match result:
      case Continue():
        pass
      case _:  # pragma: no cover
        pytest.fail("Unexpected result")
