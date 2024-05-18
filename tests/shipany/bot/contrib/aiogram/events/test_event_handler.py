import pytest
from aiogram.methods import SendMessage
from aiogram.types import Message

from shipany.bot.contrib.aiogram.context import Context
from shipany.bot.contrib.aiogram.events import AiogramEventHandler as EventHandler
from shipany.bot.conversation.loader import load


@pytest.fixture()
def event_handler(request: pytest.FixtureRequest, flow_as_fixture: str) -> EventHandler:
  flow_as_str: str = request.getfixturevalue(flow_as_fixture)
  flow = load(flow_as_str)
  return EventHandler(flow.conversations[0].steps, begin_with_step_id=flow.conversations[0].activations[0].next_step)


@pytest.mark.asyncio()
@pytest.mark.parametrize("flow_as_fixture", ["valid_flow_with_conditional_responses"])
async def test_it_responds_hey_there(event_handler: EventHandler, hi_message: Message) -> None:
  result = await event_handler(Context(event=hi_message))
  assert isinstance(result, SendMessage)
  assert result.text.startswith("Hey there")


@pytest.mark.asyncio()
@pytest.mark.parametrize("flow_as_fixture", ["valid_flow_with_conditional_responses"])
async def test_it_responds_with_emoji(event_handler: EventHandler, hello_message: Message) -> None:
  result = await event_handler(Context(event=hello_message))
  assert isinstance(result, SendMessage)
  assert result.text == "👋!"
