from pathlib import Path

import pytest

from shipany.bot import errors, loader


@pytest.mark.parametrize(
  "flows_file",
  [
    "valid_flow_with_simple_user_input_and_conditional_response.json",
    "valid_flow_with_simple_user_input.json",
    "valid_flow_with_string_substitution.json",
  ],
)
def test_basic_flows(flows_path: Path, flows_file: str) -> None:
  path = flows_path / flows_file
  json_data = path.read_text()
  try:
    loader.load(json_data)
  except errors.FlowValidationError as e:  # pragma: no cover
    pytest.fail(f"Flow validation failed: {e}")


@pytest.mark.parametrize(
  "flows_file",
  [
    "invalid_flow_with_missed_start_state.json",
    "invalid_flow_with_missed_commands.json",
  ],
)
def test_edge_case_flows(flows_path: Path, flows_file: str) -> None:
  path = flows_path / flows_file
  json_data = path.read_text()
  try:
    loader.load(json_data)
  except errors.FlowValidationError:
    pass
  except Exception as e:  # pragma: no cover
    pytest.fail(f"Flow validation should have failed with FlowValidationError but failed with another exception: {e}")
  else:  # pragma: no cover
    pytest.fail(f"Flow validation should have failed but it didn't. Input: {flows_file}")
