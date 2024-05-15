import pytest

from shipany.bot.conversation.v1.models.actions import MessageAction


@pytest.mark.parametrize(
  "content",
  [
    '{"type": "message", "content":"Hello, World!"}',
  ],
)
def test_message_action_errors_validation(content: str) -> None:
  with pytest.raises(ValueError, match="action type"):
    MessageAction.model_validate_json(content)
