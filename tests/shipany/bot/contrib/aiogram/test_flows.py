import pytest
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
