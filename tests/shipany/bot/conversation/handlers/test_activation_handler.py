import pytest

from shipany.bot.conversation import errors
from shipany.bot.conversation.context import conversation_context
from shipany.bot.conversation.errors import ActionNotImplementedError
from shipany.bot.conversation.handlers.activations import ActivationHandler
from shipany.bot.conversation.models.conversation import Conversation
from shipany.bot.conversation.models.flow import Flow


@pytest.mark.parametrize(
  "flow_as_fixture",
  [
    "valid_flow_with_unknown_action",
    "valid_flow_with_broken_v1_action",
    "valid_flow_with_broken_v2_action",
    "valid_flow_with_broken_v3_action",
    "valid_flow_with_broken_v4_action",
  ],
)
async def test_it_raises_when_unknown_action_met(flow_from_fixture: Flow) -> None:
  async with conversation_context() as default_context:
    handler = ActivationHandler(default_context, flow_from_fixture.conversations[0].activations[0])
    with pytest.raises(ActionNotImplementedError):
      await handler(flow_from_fixture.conversations[0].steps)


@pytest.mark.parametrize("flow_as_fixture", ["valid_flow_with_store_action"])
async def test_it_returns_nothing_on_empty_step(flow_from_fixture: Flow) -> None:
  async with conversation_context() as default_context:
    handler = ActivationHandler(default_context, flow_from_fixture.conversations[0].activations[0])
    await handler(flow_from_fixture.conversations[0].steps)


async def test_actions_on_step_enter_happy_path() -> None:
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
    async with conversation_context() as default_context:
      navigator = ActivationHandler(default_context, activation)
      actions = list(navigator.traverse_actions(conversation.steps))
      assert len(actions) == 1


async def test_empty_actions_in() -> None:
  conversation = Conversation.model_validate(
    {
      "$id": "start",
      "activations": [{"command": "/start", "next-step": "start"}],
      "steps": [{"$id": "start", "actions": []}],
    }
  )
  assert len(conversation.activations) == 1

  for activation in conversation.activations:
    async with conversation_context() as default_context:
      navigator = ActivationHandler(default_context, activation)
      assert len(list(navigator.traverse_actions(conversation.steps))) == 0


async def test_actions_on_step_enter_no_step() -> None:
  conversation = Conversation.model_validate(
    {
      "$id": "start",
      "activations": [{"command": "/start", "next-step": "start"}],
      "steps": [],
    }
  )
  assert len(conversation.activations) == 1
  try:
    async with conversation_context() as default_context:
      navigator = ActivationHandler(default_context, conversation.activations[0])
      list(navigator.traverse_actions(conversation.steps))
    pytest.fail("Expected exception but none was raised")  # pragma: no cover
  except errors.NoStepFoundError:
    pass


async def test_termination_at_first_step() -> None:
  conversation = Conversation.model_validate(
    {
      "$id": "start",
      "activations": [{"command": "/start", "next-step": "start"}],
      "steps": [
        {
          "$id": "start",
          "actions": [
            {
              "name": "JsonPathAction@1",
              "expression": "$.world",
              "input": "invalid",
              "captures": {"result": ""},
            },
            {"name": "TransitionAction@1", "next-step": "next"},
          ],
        },
        {
          "$id": "next",
          "actions": [{"name": "StateAction@1", "type": "store", "key": "greet", "value": "Hello, World!"}],
        },
      ],
    }
  )
  assert len(conversation.activations) == 1

  for activation in conversation.activations:
    async with conversation_context() as default_context:
      handler = ActivationHandler(default_context, activation)
      await handler(conversation.steps)


async def test_transition_to_next_step() -> None:
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
    async with conversation_context() as default_context:
      handler = ActivationHandler(default_context, activation)
      await handler(conversation.steps)
