from __future__ import annotations

from typing_extensions import Self

from pydantic import Field, model_validator

from shipany.bot.jsonlogic import JsonLogic  # noqa: TCH001

from .base import BaseAction


class TransitionAction(BaseAction):
  next_step: str = Field(alias="next-step")
  condition: JsonLogic | None = None

  @model_validator(mode="after")
  def check_type(self: Self) -> Self:
    if self.action_type != "transition":
      raise ValueError(f"The action type must be 'transition'. Supplied: {self.action_type}")
    return self
