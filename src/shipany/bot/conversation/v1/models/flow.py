from __future__ import annotations

from typing_extensions import Self

from pydantic import BaseModel, Field, field_validator

from .conversation import Conversation  # noqa: TCH001


class Flow(BaseModel):
  self_schema: str = Field(alias="$schema")
  name: str
  description: str
  version: str
  conversations: list[Conversation]

  @field_validator("self_schema")
  @classmethod
  def self_schema_is_v1(cls: type[Self], v: str) -> str:
    if not v.startswith("https://shipany.bot/schemas/bot/v1."):
      raise ValueError("Wrong schema version")
    return v
