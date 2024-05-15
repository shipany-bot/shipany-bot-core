from enum import StrEnum
from typing_extensions import Self

from pydantic import model_validator

from .base import BaseAction


class SupportedMessageActionTypes(StrEnum):
  answer = "answer"
  reply = "reply"


class MessageAction(BaseAction):
  content: str

  @model_validator(mode="after")
  def check_type(self: Self) -> Self:
    if self.action_type not in {*SupportedMessageActionTypes}:
      raise ValueError(
        f"The action type must be one of: {[x.name for x in SupportedMessageActionTypes]}. Supplied: {self.action_type}"
      )
    return self
