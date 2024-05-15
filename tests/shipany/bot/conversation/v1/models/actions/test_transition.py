import pytest

from shipany.bot.conversation.v1.models.actions import TransitionAction


@pytest.mark.parametrize(
  "content",
  [
    '{"type": "trans", "next-step":"Hello"}',
  ],
)
def test_message_action_errors_validation(content: str) -> None:
  with pytest.raises(ValueError, match="action type"):
    TransitionAction.model_validate_json(content)
