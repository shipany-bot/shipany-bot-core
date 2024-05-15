from __future__ import annotations

from pydantic import BaseModel, Field

from shipany.bot.jsonlogic import JsonLogic  # noqa: TCH001


class BaseActivation(BaseModel):
  next_step: str = Field(alias="next-step")
  condition: JsonLogic | None = None
