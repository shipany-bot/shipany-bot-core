from __future__ import annotations

from pydantic import BaseModel, Field

from .activations import Activations  # noqa: TCH001
from .steps import Steps  # noqa: TCH001


class Conversation(BaseModel):
  """Conversation model. Describes a single conversation flow - a sequence of
  steps activated by some activity in the messenger."""

  conversation_id: str = Field(alias="$id", description="Unique conversation identifier.")
  activations: Activations = Field(description="List of activations that trigger the conversation steps.")
  steps: Steps = Field(description="List of steps in the conversation.")
