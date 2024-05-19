from __future__ import annotations

import typing as t
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class SupportedStateActionTypes(StrEnum):
  store = "store"


class StateAction(BaseModel):
  name: t.Literal["StateAction@1"]
  action_type: SupportedStateActionTypes = Field(alias="type")
  key: str
  value: str | None = None
  model_config = ConfigDict(extra="allow", frozen=True)
