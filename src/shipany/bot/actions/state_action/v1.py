from __future__ import annotations

import typing as t
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SupportedStateActionTypes(StrEnum):
  remove = "remove"
  store = "store"


class StateAction(BaseModel):
  """Action to store or retrieve a state."""

  name: t.Literal["StateAction@1"]
  """Action name."""

  action_type: SupportedStateActionTypes = Field(alias="type")
  """Action type."""

  key: str
  """Name of state to store or retrieve."""

  value: str | None = None
  """Value to store. It can't be None if action_type is store."""

  model_config = ConfigDict(extra="allow", frozen=True)

  @model_validator(mode="after")
  def validate_value(self: t.Self) -> t.Self:
    if self.action_type == SupportedStateActionTypes.store and self.value is None:
      raise ValueError("Value cannot be None for 'store' action type.")
    return self
