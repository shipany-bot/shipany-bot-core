from __future__ import annotations

import datetime
import typing as t

import pytest
from aiogram.types import Chat, Message

from shipany.bot.conversation.context import ConversationContext, conversation_context
from shipany.bot.conversation.handlers.actions import AwaitObjectAndContinue, Continue, GoToStep, Terminate, handle
from shipany.bot.conversation.models.action import BaseAction

if t.TYPE_CHECKING:
  from pytest_httpx import HTTPXMock


@pytest.fixture()
async def default_context(hello_message: Message) -> t.AsyncIterator[ConversationContext]:
  async with conversation_context(event=hello_message) as ctx:
    yield ctx


async def test_action_executor_dispatch_unsupported_action() -> None:
  message = Message(
    message_id=1, date=datetime.datetime.now(tz=datetime.timezone.utc), chat=Chat(id=1, type="private", username="test")
  )
  async with conversation_context(event=message) as ctx:
    action = BaseAction(name="unsupported@1")
    with pytest.raises(NotImplementedError, match="is not importable"):
      await handle(action, ctx)


async def test_action_executor_dispatch_answer(default_context: ConversationContext) -> None:
  action = BaseAction.model_validate({"name": "MessageAction@1", "type": "answer", "content": "Hello, World!"})
  result = await handle(action, default_context)
  assert isinstance(result, AwaitObjectAndContinue)


async def test_action_executor_dispatch_reply(default_context: ConversationContext) -> None:
  action = BaseAction.model_validate({"name": "MessageAction@1", "type": "reply", "content": "Hello, World!"})
  result = await handle(action, default_context)
  assert isinstance(result, AwaitObjectAndContinue)


async def test_action_executor_dispatch_transition(default_context: ConversationContext) -> None:
  action = BaseAction.model_validate({"name": "TransitionAction@1", "next-step": "hello", "condition": None})
  result = await handle(action, default_context)

  assert isinstance(result, GoToStep)


async def test_action_executor_dispatch_store(default_context: ConversationContext) -> None:
  action = BaseAction.model_validate({"name": "StateAction@1", "type": "store", "key": "hello", "value": "world"})
  result = await handle(action, default_context)

  assert isinstance(result, Continue)


async def test_awaitable_handler(httpx_mock: HTTPXMock, default_context: ConversationContext) -> None:
  httpx_mock.add_response(url="http://localhost:7812/post", method="POST", text="response text")

  action = BaseAction.model_validate(
    {
      "name": "HttpRequest@1",
      "url": "http://localhost:7812/post",
      "method": "POST",
      "headers": {"Content-Type": "application/json"},
      "body": {"foo": "bar"},
    },
  )
  result = await handle(action, default_context)
  assert isinstance(result, Continue)


async def test_handler_can_terminate(default_context: ConversationContext) -> None:
  action = BaseAction.model_validate(
    {
      "name": "JsonPathAction@1",
      "expression": "$.world",
      "input": "invalid",
      "captures": {"result": ""},
    }
  )
  result = await handle(action, default_context)
  assert isinstance(result, Terminate)
