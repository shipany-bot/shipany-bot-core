import json
from unittest.mock import AsyncMock, Mock

import pytest
from aiogram import methods
from aiogram.types import Message

from shipany.bot.conversation.context import conversation_context
from shipany.bot.conversation.handlers.activations import ActivationHandler
from shipany.bot.conversation.models.flow import Flow


@pytest.mark.asyncio()
@pytest.mark.parametrize("flow_as_fixture", ["valid_flow_with_conditional_responses"])
async def test_transition_to_next_step_with_condition(flow_from_fixture: Flow, hi_message: Message) -> None:
  with conversation_context(event=hi_message) as ctx:
    handler = ActivationHandler(ctx, flow_from_fixture.conversations[0].activations[0])
    await handler(flow_from_fixture.conversations[0].steps)


@pytest.fixture()
def valid_flow_with_echoing() -> str:
  return json.dumps(
    {
      "$schema": "https://shipany.bot/schemata/0.1.0/schema.json",
      "name": "echo-bot",
      "description": "",
      "version": "1.0.0",
      "conversations": [
        {
          "$id": "start",
          "activations": [{"event": "on-message", "next-step": "start"}],
          "steps": [
            {"$id": "start", "actions": [{"name": "MessageAction@1", "type": "reply", "content": "{{message.text}}"}]},
          ],
        }
      ],
    }
  )


@pytest.mark.asyncio()
@pytest.mark.parametrize("flow_as_fixture", ["valid_flow_with_echoing"])
async def test_awaiting_step(hi_message: Message, flow_from_fixture: Flow, monkeypatch: pytest.MonkeyPatch) -> None:
  conversation = flow_from_fixture.conversations[0]
  assert len(conversation.activations) == 1

  mocked_send_message = Mock()
  mocked_send_message.return_value = AsyncMock()

  monkeypatch.setattr(methods, "SendMessage", mocked_send_message)
  for activation in conversation.activations:
    with conversation_context(hi_message) as default_context:
      handler = ActivationHandler(default_context, activation)
      await handler(conversation.steps)
