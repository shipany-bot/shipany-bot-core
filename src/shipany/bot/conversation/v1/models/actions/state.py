from __future__ import annotations

from enum import StrEnum
from typing_extensions import Self

from pydantic import model_validator

from .base import BaseAction


class SupportedStateActionTypes(StrEnum):
  store = "store"


class StateAction(BaseAction):
  key: str
  value: str | None = None

  @model_validator(mode="after")
  def check_type(self: Self) -> Self:
    if self.action_type not in {*SupportedStateActionTypes}:
      raise ValueError(
        f"The action type must be one of: {[x.name for x in SupportedStateActionTypes]}. Supplied: {self.action_type}"
      )
    return self
