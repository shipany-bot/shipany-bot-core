import datetime

import pytest
from aiogram.types import Chat, Message

from shipany.bot.contrib.aiogram.action_dispatcher import handle
from shipany.bot.contrib.aiogram.context import Context
from shipany.bot.conversation.models.v1.action import BaseAction


@pytest.mark.asyncio()
async def test_action_executor_dispatch_unsupported_action() -> None:
  message = Message(
    message_id=1, date=datetime.datetime.now(tz=datetime.timezone.utc), chat=Chat(id=1, type="private", username="test")
  )
  ctx = Context(event=message, captures={})
  action = BaseAction(name="unsupported@1")
  with pytest.raises(NotImplementedError, match="is not importable"):
    await handle(action, ctx)


@pytest.mark.asyncio()
async def test_action_executor_dispatch_answer(hello_message: Message) -> None:
  ctx = Context(event=hello_message, captures={})

  action = BaseAction(**{"name": "MessageAction@1", "type": "answer", "content": "Hello, World!"})
  result = await handle(action, ctx)

  assert result is not None


@pytest.mark.asyncio()
async def test_action_executor_dispatch_reply(hello_message: Message) -> None:
  ctx = Context(event=hello_message, captures={})
  action = BaseAction(**{"name": "MessageAction@1", "type": "reply", "content": "Hello, World!"})
  result = await handle(action, ctx)

  assert result is not None


@pytest.mark.asyncio()
async def test_action_executor_dispatch_transition(hello_message: Message) -> None:
  ctx = Context(event=hello_message, captures={})
  action = BaseAction(**{"name": "TransitionAction@1", "next-step": "hello", "condition": None})
  result = await handle(action, ctx)

  assert result is not None


@pytest.mark.asyncio()
async def test_action_executor_dispatch_store(hello_message: Message) -> None:
  ctx = Context(event=hello_message, captures={})
  action = BaseAction(**{"name": "StateAction@1", "type": "store", "key": "hello", "value": "world"})
  result = await handle(action, ctx)

  assert result is not None
