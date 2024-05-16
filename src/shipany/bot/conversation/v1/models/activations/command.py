from typing_extensions import Self

from pydantic import Field, model_validator

from .base import BaseActivation


class CommandActivation(BaseActivation):
  """Describes a command that triggers the conversation."""

  command: str = Field(min_length=1, max_length=32, description="Command name.", examples=["start", "help"])
  prefix: str = Field(default="", max_length=1, description="Command prefix.", examples=["/", "!"])

  @model_validator(mode="after")
  def check_command_prefix(self: Self) -> Self:
    if self.prefix == "":
      prefix = self.command[:1]
      # Check if the prefix is included in the command
      if prefix and not prefix.isalpha():
        # Split the command into prefix and command name
        self.prefix = prefix
        self.command = self.command[1:]
      else:
        raise ValueError("The prefix must not be empty.")
    else:
      # Check if the prefix is included in the command
      if not self.command[:1].isalpha():
        raise ValueError("The prefix must not be a part of command.")
      if self.prefix.isalpha():
        raise ValueError("The prefix must be a non-alphabetic character.")
    return self
