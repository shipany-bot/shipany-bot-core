import datetime
import typing as t

import pytest
from aiogram.types import Chat, Message

from shipany.bot.conversation.context import ConversationContext, conversation_context
from shipany.bot.conversation.handlers.actions import handle
from shipany.bot.conversation.models.action import BaseAction


@pytest.fixture()
def default_context(hello_message: Message) -> t.Iterator[ConversationContext]:
  with conversation_context(event=hello_message) as ctx:
    yield ctx


@pytest.mark.asyncio()
async def test_action_executor_dispatch_unsupported_action() -> None:
  message = Message(
    message_id=1, date=datetime.datetime.now(tz=datetime.timezone.utc), chat=Chat(id=1, type="private", username="test")
  )
  with conversation_context(event=message) as ctx:
    action = BaseAction(name="unsupported@1")
    with pytest.raises(NotImplementedError, match="is not importable"):
      await handle(action, ctx)


@pytest.mark.asyncio()
async def test_action_executor_dispatch_answer(default_context: ConversationContext) -> None:
  action = BaseAction.model_validate({"name": "MessageAction@1", "type": "answer", "content": "Hello, World!"})
  await handle(action, default_context)


@pytest.mark.asyncio()
async def test_action_executor_dispatch_reply(default_context: ConversationContext) -> None:
  action = BaseAction.model_validate({"name": "MessageAction@1", "type": "reply", "content": "Hello, World!"})
  await handle(action, default_context)


@pytest.mark.asyncio()
async def test_action_executor_dispatch_transition(default_context: ConversationContext) -> None:
  action = BaseAction.model_validate({"name": "TransitionAction@1", "next-step": "hello", "condition": None})
  result = await handle(action, default_context)

  assert result is not None


@pytest.mark.asyncio()
async def test_action_executor_dispatch_store(default_context: ConversationContext) -> None:
  action = BaseAction.model_validate({"name": "StateAction@1", "type": "store", "key": "hello", "value": "world"})
  result = await handle(action, default_context)

  assert result is not None
