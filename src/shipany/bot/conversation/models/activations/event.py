from __future__ import annotations

import typing as t

from pydantic import Field, field_validator

from .base import BaseActivation


class EventActivation(BaseActivation):
  """Describes an event that triggers the conversation. Commonly used for message events."""

  event: str = Field(
    description="List of supported event names that can trigger the conversation steps.",
  )

  @field_validator("event")
  @classmethod
  def validate_event(cls: type[t.Self], value: str) -> str:
    if not value.startswith("on-"):
      raise ValueError("Event name must start with 'on-'")
    return value
