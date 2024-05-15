from __future__ import annotations

from typing_extensions import Self

from pydantic import Field, field_validator

from .base import BaseAction


class FunctionAction(BaseAction):
  call: str
  args: list[str]
  capture: str | None = Field(None, min_length=2)

  @field_validator("capture")
  @classmethod
  def check_capture(cls: type[Self], v: str) -> str:
    if not v.startswith("$"):
      raise ValueError("The capture variable must start with '$'.")
    return v
