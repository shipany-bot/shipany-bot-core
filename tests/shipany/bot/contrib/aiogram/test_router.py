from __future__ import annotations

import typing as t

import pytest
from aiogram.dispatcher.event.bases import SkipHandler

from shipany.bot.contrib.aiogram.events import AiogramEventHandler as EventHandler
from shipany.bot.contrib.aiogram.router import create, handler
from shipany.bot.conversation import errors
from shipany.bot.conversation.models.v1.activations import Activation, EventActivation
from shipany.bot.conversation.models.v1.conversation import Conversation
from shipany.bot.conversation.models.v1.flow import Flow
from shipany.bot.conversation.models.v1.steps import Step

if t.TYPE_CHECKING:
  from aiogram.types import Message


@pytest.fixture(autouse=True)
def _set_runtime_injections() -> None:
  import inject

  from shipany.bot.runtime.bindings import default_runtime_injections

  inject.clear_and_configure(default_runtime_injections)


def test_create_nested_router_with_no_conversations() -> None:
  flow = Flow(
    **{
      "$schema": "https://shipany.bot/schemata/0.1.0/schema.json",
      "name": "Test",
      "description": "Test",
      "version": "0.1.0",
      "conversations": [],
    }
  )
  try:
    create(flow=flow)
  except Exception:  # pragma: no cover
    pytest.fail("Unexpected exception")


def test_create_nested_router_with_one_conversation() -> None:
  flow = Flow(
    **{
      "$schema": "https://shipany.bot/schemata/0.1.0/schema.json",
      "name": "Test",
      "description": "Test",
      "version": "0.1.0",
      "conversations": [
        {
          "$id": "start",
          "activations": [{"command": "/start", "next-step": "start"}],
          "steps": [
            {"$id": "start", "actions": [{"name": "MessageAction@1", "type": "answer", "content": "Hello, World!"}]}
          ],
        }
      ],
    }
  )
  try:
    create(flow=flow)
  except Exception:  # pragma: no cover
    pytest.fail("Unexpected exception")


def test_actions_on_step_enter_happy_path() -> None:
  conversation = Conversation(
    **{
      "$id": "start",
      "activations": [{"command": "/start", "next-step": "start"}],
      "steps": [
        {"$id": "start", "actions": [{"name": "MessageAction@1", "type": "answer", "content": "Hello, World!"}]}
      ],
    }
  )
  assert len(conversation.activations) == 1

  for activation in conversation.activations:
    navigator = EventHandler(conversation.steps, begin_with_step_id=activation.next_step)
    actions = list(navigator.traverse_actions())
    assert len(actions) == 1


def test_empty_actions_in() -> None:
  conversation = Conversation(
    **{
      "$id": "start",
      "activations": [{"command": "/start", "next-step": "start"}],
      "steps": [{"$id": "start", "actions": []}],
    }
  )
  assert len(conversation.activations) == 1

  for activation in conversation.activations:
    navigator = EventHandler(conversation.steps, begin_with_step_id=activation.next_step)
    assert len(list(navigator.traverse_actions())) == 0


def test_actions_on_step_enter_no_step() -> None:
  conversation = Conversation(
    **{
      "$id": "start",
      "activations": [{"command": "/start", "next-step": "start"}],
      "steps": [],
    }
  )
  try:
    assert len(conversation.activations) == 1

    for activation in conversation.activations:
      navigator = EventHandler(conversation.steps, begin_with_step_id=activation.next_step)
      list(navigator.traverse_actions())
    pytest.fail("Expected exception but none was raised")  # pragma: no cover
  except errors.NoStepFoundError:
    pass


@pytest.mark.parametrize(
  "activation",
  [
    (
      EventActivation(
        **{"event": "on-message", "next-step": "$1", "condition": {"==": [{"var": "message.text"}, "hi"]}}
      )
    ),
  ],
)
@pytest.mark.asyncio()
async def test_handle_failed_conditional_event(activation: Activation, hello_message: Message) -> None:
  steps = [Step(**{"$id": "$1", "actions": [{"name": "MessageAction@1", "type": "reply", "content": "Hello"}]})]
  with pytest.raises(SkipHandler):
    await handler(activation, steps, event=hello_message)


# @pytest.mark.parametrize(
#   ("activation", "expected_instance"),
#   [
#     (CommandActivation(**{"command": "/start", "next-step": "$1", "condition": None}), SendMessage),
#     (EventActivation(**{"event": "on-message", "next-step": "$1", "condition": None}), SendMessage),
#     (
#       EventActivation(
#         **{"event": "on-message", "next-step": "$1", "condition": {"==": [{"var": "message.text"}, "Hello"]}}
#       ),
#       SendMessage,
#     ),
#   ],
# )
# @pytest.mark.asyncio()
# async def test_handle_conditional_event(
#   activation: Activation, hello_message: Message, expected_instance: type[TelegramMethod]
# ) -> None:
#   steps = [Step(**{"$id": "$1", "actions": [{"name": "MessageAction@1", "type": "reply", "content": "Hello"}]})]
#   await handler(activation, steps, event=hello_message)
