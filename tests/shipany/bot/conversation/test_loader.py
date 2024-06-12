from pathlib import Path

import pytest

from shipany.bot import errors, loader


@pytest.mark.parametrize(
  "flow_filename",
  [
    "valid_flow_with_simple_user_input_and_conditional_response.json",
    "valid_flow_with_simple_user_input.json",
    "valid_flow_with_string_substitution.json",
  ],
)
def test_basic_flows(v1_flow_fixtures_location: Path, flow_filename: str) -> None:
  path = v1_flow_fixtures_location / flow_filename
  json_data = path.read_text()
  try:
    loader.load(json_data)
  except errors.FlowValidationError as e:  # pragma: no cover
    pytest.fail(f"Flow validation failed: {e}")


@pytest.mark.parametrize(
  "flow_filename",
  [
    "invalid_flow_with_missed_start_state.json",
    "invalid_flow_with_missed_commands.json",
  ],
)
def test_edge_case_flows(v1_flow_fixtures_location: Path, flow_filename: str) -> None:
  path = v1_flow_fixtures_location / flow_filename
  json_data = path.read_text()
  try:
    loader.load(json_data)
  except errors.FlowValidationError:
    pass
  except Exception as e:  # pragma: no cover
    pytest.fail(f"Flow validation should have failed with FlowValidationError but failed with another exception: {e}")
  else:  # pragma: no cover
    pytest.fail(f"Flow validation should have failed but it didn't. Input: {flow_filename}")
