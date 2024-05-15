import datetime

import pytest
from aiogram.types import Chat, Message
from pydantic import ValidationError

from shipany.bot.contrib.aiogram.action_dispatcher import handle
from shipany.bot.contrib.aiogram.context import Context
from shipany.bot.conversation.v1.models import (
  BaseAction,
  FunctionAction,
  MessageAction,
  StateAction,
  TransitionAction,
)


@pytest.mark.asyncio()
async def test_action_executor_dispatch_unsupported_action() -> None:
  message = Message(
    message_id=1, date=datetime.datetime.now(tz=datetime.timezone.utc), chat=Chat(id=1, type="private", username="test")
  )
  ctx = Context(event=message, captures={})
  action = BaseAction(type="unsupported")
  try:
    await handle(action, ctx)
    pytest.fail("Expected exception but none was raised")  # pragma: no cover
  except ValidationError:
    pass
  except Exception:  # pragma: no cover
    pytest.fail("Unexpected exception")


@pytest.mark.asyncio()
async def test_action_executor_dispatch_answer(hello_message: Message) -> None:
  ctx = Context(event=hello_message, captures={})

  action = MessageAction(type="answer", content="Hello, World!")
  result = await handle(action, ctx)

  assert result is not None


@pytest.mark.asyncio()
async def test_action_executor_dispatch_reply(hello_message: Message) -> None:
  ctx = Context(event=hello_message, captures={})
  action = MessageAction(type="reply", content="Hello, World!")
  result = await handle(action, ctx)

  assert result is not None


@pytest.mark.asyncio()
async def test_action_executor_dispatch_transition(hello_message: Message) -> None:
  ctx = Context(event=hello_message, captures={})
  action = TransitionAction(**{"type": "transition", "next-step": "hello", "condition": None})
  result = await handle(action, ctx)

  assert result is not None


@pytest.mark.asyncio()
async def test_action_executor_dispatch_function(hello_message: Message) -> None:
  ctx = Context(event=hello_message, captures={})
  action = FunctionAction(**{"type": "function", "call": "echo", "args": ["Hello World"]})
  result = await handle(action, ctx)

  assert result is not None


@pytest.mark.asyncio()
async def test_action_executor_dispatch_store(hello_message: Message) -> None:
  ctx = Context(event=hello_message, captures={})
  action = StateAction(**{"type": "store", "key": "hello", "value": "world"})
  result = await handle(action, ctx)

  assert result is not None
