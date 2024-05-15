from __future__ import annotations

from pydantic import BaseModel, Field

from .activations import Activations  # noqa: TCH001
from .steps import Steps  # noqa: TCH001


class Conversation(BaseModel):
  conversation_id: str = Field(alias="$id")
  activations: Activations
  steps: Steps
