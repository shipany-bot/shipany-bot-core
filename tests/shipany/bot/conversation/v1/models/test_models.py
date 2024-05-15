import pytest

from shipany.bot.conversation.v1.models import CommandActivation, Flow


def test_schema_checked() -> None:
  with pytest.raises(ValueError, match="schema"):
    Flow(
      **{"$schema": "http://example.com", "name": "Test", "description": "Test", "version": "0.1", "conversations": []}
    )


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
    CommandActivation(**{"command": command, "prefix": prefix, "next-step": "test"})
