import pytest

# from aiogram.methods import SendMessage
from aiogram.types import Message

from shipany.bot.contrib.aiogram.context import Context
from shipany.bot.contrib.aiogram.events import AiogramEventHandler as EventHandler
from shipany.bot.conversation.loader import load
from shipany.bot.errors import ActionNotImplementedError


@pytest.fixture()
def event_handler(request: pytest.FixtureRequest, flow_as_fixture: str) -> EventHandler:
  flow_as_str: str = request.getfixturevalue(flow_as_fixture)
  flow = load(flow_as_str)
  return EventHandler(flow.conversations[0].steps, begin_with_step_id=flow.conversations[0].activations[0].next_step)


# @pytest.mark.asyncio()
# @pytest.mark.parametrize("flow_as_fixture", ["valid_flow_with_conditional_responses"])
# async def test_it_responds_hey_there(event_handler: EventHandler, hi_message: Message) -> None:
#   await event_handler(Context(event=hi_message))


@pytest.mark.asyncio()
@pytest.mark.parametrize(
  "flow_as_fixture",
  ["valid_flow_with_unknown_action", "valid_flow_with_broken_v1_action", "valid_flow_with_broken_v2_action"],
)
async def test_it_raises_when_unknown_action_met(event_handler: EventHandler, hello_message: Message) -> None:
  with pytest.raises(ActionNotImplementedError):
    await event_handler(Context(event=hello_message))


# @pytest.mark.asyncio()
# @pytest.mark.parametrize("flow_as_fixture", ["valid_flow_with_conditional_responses"])
# async def test_it_responds_with_emoji(event_handler: EventHandler, hello_message: Message) -> None:
#   await event_handler(Context(event=hello_message))


@pytest.mark.asyncio()
@pytest.mark.parametrize("flow_as_fixture", ["valid_flow_with_store_action"])
async def test_it_returns_nothing_on_empty_step(event_handler: EventHandler, hello_message: Message) -> None:
  result = await event_handler(Context(event=hello_message))
  assert result is None
