import pytest

from shipany.bot.contrib.aiogram.actions.state import StateAction


def test_state_action_errors_validation() -> None:
  with pytest.raises(ValueError, match="action type"):
    StateAction.model_validate_json('{"type": "state", "key": "key"}')
