import pytest

from shipany.bot.conversation import errors
from shipany.bot.conversation.errors import ActionNotImplementedError
from shipany.bot.conversation.handlers.activations import ActivationHandler
from shipany.bot.conversation.models.conversation import Conversation
from shipany.bot.conversation.models.flow import Flow
from shipany.bot.runtime.context import Context


@pytest.fixture()
def default_context() -> Context:
  return Context()


@pytest.mark.asyncio()
@pytest.mark.parametrize(
  "flow_as_fixture",
  ["valid_flow_with_unknown_action", "valid_flow_with_broken_v1_action", "valid_flow_with_broken_v2_action"],
)
async def test_it_raises_when_unknown_action_met(default_context: Context, flow_from_fixture: Flow) -> None:
  handler = ActivationHandler(default_context, flow_from_fixture.conversations[0].activations[0])
  with pytest.raises(ActionNotImplementedError):
    await handler(flow_from_fixture.conversations[0].steps)


@pytest.mark.asyncio()
@pytest.mark.parametrize("flow_as_fixture", ["valid_flow_with_store_action"])
async def test_it_returns_nothing_on_empty_step(default_context: Context, flow_from_fixture: Flow) -> None:
  handler = ActivationHandler(default_context, flow_from_fixture.conversations[0].activations[0])
  await handler(flow_from_fixture.conversations[0].steps)


def test_actions_on_step_enter_happy_path(default_context: Context) -> None:
  conversation = Conversation.model_validate(
    {
      "$id": "start",
      "activations": [{"command": "/start", "next-step": "start"}],
      "steps": [
        {"$id": "start", "actions": [{"name": "MessageAction@1", "type": "answer", "content": "Hello, World!"}]}
      ],
    }
  )
  assert len(conversation.activations) == 1

  for activation in conversation.activations:
    navigator = ActivationHandler(default_context, activation)
    actions = list(navigator.traverse_actions(conversation.steps))
    assert len(actions) == 1


def test_empty_actions_in(default_context: Context) -> None:
  conversation = Conversation.model_validate(
    {
      "$id": "start",
      "activations": [{"command": "/start", "next-step": "start"}],
      "steps": [{"$id": "start", "actions": []}],
    }
  )
  assert len(conversation.activations) == 1

  for activation in conversation.activations:
    navigator = ActivationHandler(default_context, activation)
    assert len(list(navigator.traverse_actions(conversation.steps))) == 0


def test_actions_on_step_enter_no_step(default_context: Context) -> None:
  conversation = Conversation.model_validate(
    {
      "$id": "start",
      "activations": [{"command": "/start", "next-step": "start"}],
      "steps": [],
    }
  )
  try:
    assert len(conversation.activations) == 1

    for activation in conversation.activations:
      navigator = ActivationHandler(default_context, activation)
      list(navigator.traverse_actions(conversation.steps))
    pytest.fail("Expected exception but none was raised")  # pragma: no cover
  except errors.NoStepFoundError:
    pass


@pytest.mark.asyncio()
async def test_transition_to_next_step(default_context: Context) -> None:
  conversation = Conversation.model_validate(
    {
      "$id": "start",
      "activations": [{"command": "/start", "next-step": "start"}],
      "steps": [
        {"$id": "start", "actions": [{"name": "TransitionAction@1", "next-step": "next"}]},
        {
          "$id": "next",
          "actions": [{"name": "StateAction@1", "type": "store", "key": "greet", "value": "Hello, World!"}],
        },
      ],
    }
  )
  assert len(conversation.activations) == 1

  for activation in conversation.activations:
    handler = ActivationHandler(default_context, activation)
    await handler(conversation.steps)
