import pytest
from pydantic import ValidationError

from shipany.bot.actions.state_action.v1 import StateAction


def test_store_type_with_no_value() -> None:
  with pytest.raises(ValidationError, match="Value cannot be None for 'store' action type"):
    StateAction.model_validate(
      {
        "name": "StateAction@1",
        "type": "store",
        "key": "key",
      }
    )


def test_remove_type_with_value() -> None:
  try:
    StateAction.model_validate(
      {
        "name": "StateAction@1",
        "type": "remove",
        "key": "key",
        "value": "value",
      }
    )
  except ValidationError:  # pragma: no cover
    pytest.fail("Unexpected ValidationError")
