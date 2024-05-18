from __future__ import annotations

import typing as t

from pydantic import BaseModel, Field

from shipany.bot.jsonlogic import JsonLogic  # noqa: TCH001


class TransitionAction(BaseModel):
  name: t.Literal["TransitionAction@1"]
  next_step: str = Field(alias="next-step")
  condition: JsonLogic | None = None
