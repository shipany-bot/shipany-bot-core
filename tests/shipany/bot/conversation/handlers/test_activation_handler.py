import pytest

from shipany.bot.conversation.errors import ActionNotImplementedError
from shipany.bot.conversation.handlers.activations import ActivationHandler
from shipany.bot.conversation.loader import load
from shipany.bot.conversation.models.flow import Flow
from shipany.bot.runtime.context import Context


@pytest.fixture()
def default_context() -> Context:
  return Context()


@pytest.fixture()
def flow(request: pytest.FixtureRequest, flow_as_fixture: str, default_context: Context) -> Flow:
  flow_as_str: str = request.getfixturevalue(flow_as_fixture)
  return load(flow_as_str)


@pytest.mark.asyncio()
@pytest.mark.parametrize(
  "flow_as_fixture",
  ["valid_flow_with_unknown_action", "valid_flow_with_broken_v1_action", "valid_flow_with_broken_v2_action"],
)
async def test_it_raises_when_unknown_action_met(default_context: Context, flow: Flow) -> None:
  handler = ActivationHandler(default_context, flow.conversations[0].activations[0])
  with pytest.raises(ActionNotImplementedError):
    await handler(flow.conversations[0].steps)


@pytest.mark.asyncio()
@pytest.mark.parametrize("flow_as_fixture", ["valid_flow_with_store_action"])
async def test_it_returns_nothing_on_empty_step(default_context: Context, flow: Flow) -> None:
  handler = ActivationHandler(default_context, flow.conversations[0].activations[0])
  await handler(flow.conversations[0].steps)
