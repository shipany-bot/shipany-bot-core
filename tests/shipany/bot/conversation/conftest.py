import typing as t
from pathlib import Path

import pytest

from shipany.bot.conversation.loader import load
from shipany.bot.conversation.models.flow import Flow


@pytest.fixture()
def flow_from_fixture(request: pytest.FixtureRequest, flow_as_fixture: str) -> Flow:
  flow_as_str: str = request.getfixturevalue(flow_as_fixture)
  return load(flow_as_str)


@pytest.fixture()
def v1_flow_fixtures_location(flows_path_factory: t.Callable[[int], Path]) -> Path:
  return flows_path_factory(1)
