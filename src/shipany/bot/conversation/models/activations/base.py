from __future__ import annotations

from pydantic import BaseModel, Field

from shipany.bot.jsonlogic import JsonLogic  # noqa: TCH001


class BaseActivation(BaseModel):
  next_step: str = Field(alias="next-step", title="Next step", description="Next step identifier.")
  condition: JsonLogic | None = Field(
    default=None,
    description="Condition that must be met to activate the step. Expressed in JSONLogic. Empty means always true.",
  )
