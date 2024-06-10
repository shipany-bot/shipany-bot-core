import pytest

from shipany.bot.conversation.models.activations.command import CommandActivation


@pytest.mark.parametrize(
  ("command", "prefix"),
  [
    ("test", ""),
    ("test", "t"),
    ("test", "T"),
    ("/command", "#"),
  ],
)
def test_command_prefix_invalid_values(command: str, prefix: str) -> None:
  with pytest.raises(ValueError, match="The prefix"):
    CommandActivation.model_validate({"command": command, "prefix": prefix, "next-step": "test"})
