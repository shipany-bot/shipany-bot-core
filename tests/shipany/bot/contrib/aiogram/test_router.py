from __future__ import annotations

import typing as t

import pytest
from aiogram.dispatcher.event.bases import SkipHandler

from shipany.bot.contrib.aiogram.router import create, handler
from shipany.bot.conversation.loader import load
from shipany.bot.conversation.models.activations import Activation, CommandActivation, EventActivation
from shipany.bot.conversation.models.flow import Flow
from shipany.bot.conversation.models.steps import Step

if t.TYPE_CHECKING:
  from aiogram.types import Message


def test_create_nested_router_with_no_conversations() -> None:
  flow = Flow.model_validate(
    {
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
  flow = Flow.model_validate(
    {
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


@pytest.mark.parametrize(
  "activation",
  [
    (
      EventActivation.model_validate(
        {"event": "on-message", "next-step": "$1", "condition": {"==": [{"var": "message.text"}, "hi"]}}
      )
    ),
  ],
)
@pytest.mark.asyncio()
async def test_handle_failed_conditional_event(activation: Activation, hello_message: Message) -> None:
  steps = [
    Step.model_validate({"$id": "$1", "actions": [{"name": "MessageAction@1", "type": "reply", "content": "Hello"}]})
  ]
  with pytest.raises(SkipHandler):
    await handler(activation, steps, event=hello_message)


@pytest.mark.parametrize(
  "activation",
  [
    CommandActivation.model_validate({"command": "/start", "next-step": "$1", "condition": None}),
    EventActivation.model_validate({"event": "on-message", "next-step": "$1", "condition": None}),
    EventActivation.model_validate(
      {"event": "on-message", "next-step": "$1", "condition": {"==": [{"var": "message.text"}, "Hello"]}}
    ),
  ],
)
@pytest.mark.asyncio()
async def test_handle_conditional_event(activation: Activation, hello_message: Message) -> None:
  steps = [
    Step.model_validate(
      {"$id": "$1", "actions": [{"name": "StateAction@1", "type": "store", "key": "Hello", "value": "World"}]}
    )
  ]
  await handler(activation, steps, event=hello_message)


@pytest.mark.parametrize(
  "conversation",
  [
    """{
      "$schema": "https://shipany.bot/schemata/0.1.0/schema.json",
      "name": "Test",
      "description": "Test",
      "version": "0.1.0",
      "conversations": [{
        "$id": "start",
        "activations": [
          {"command": "/start", "next-step": "start"},
          {"event": "on-message", "next-step": "start"},
          {
            "webhook": {
              "path": "/hook",
              "method": "POST",
              "status-code-ok": "200",
              "status-code-error": "400",
              "expect": {"headers": {}, "query-parameters": {}}
            },
            "next-step": "start"
          }
        ],
        "steps": [
          {
            "$id": "start",
            "actions": [{"name": "StateAction@1", "type": "store", "key": "greet", "value": "Hello, World!"}]
          }
        ]
      }]
    }"""
  ],
)
@pytest.mark.asyncio()
async def test_create_flow_with_many_activations(conversation: str) -> None:
  flow = load(conversation)
  create(flow)
