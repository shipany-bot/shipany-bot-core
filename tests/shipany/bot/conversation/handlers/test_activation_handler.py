import pytest

from shipany.bot.conversation.errors import ActionNotImplementedError
from shipany.bot.conversation.handlers.activations import ActivationHandler
from shipany.bot.conversation.loader import load
from shipany.bot.runtime.context import Context


@pytest.fixture()
def event_handler(request: pytest.FixtureRequest, flow_as_fixture: str) -> ActivationHandler:
  flow_as_str: str = request.getfixturevalue(flow_as_fixture)
  flow = load(flow_as_str)
  return ActivationHandler(
    flow.conversations[0].steps, begin_with_step_id=flow.conversations[0].activations[0].next_step
  )


@pytest.mark.asyncio()
@pytest.mark.parametrize(
  "flow_as_fixture",
  ["valid_flow_with_unknown_action", "valid_flow_with_broken_v1_action", "valid_flow_with_broken_v2_action"],
)
async def test_it_raises_when_unknown_action_met(event_handler: ActivationHandler) -> None:
  with pytest.raises(ActionNotImplementedError):
    await event_handler(Context())


@pytest.mark.asyncio()
@pytest.mark.parametrize("flow_as_fixture", ["valid_flow_with_store_action"])
async def test_it_returns_nothing_on_empty_step(event_handler: ActivationHandler) -> None:
  await event_handler(Context())
