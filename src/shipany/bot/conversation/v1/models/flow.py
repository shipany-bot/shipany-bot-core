from __future__ import annotations

from pydantic import BaseModel, Field, HttpUrl

from .conversation import Conversation  # noqa: TCH001
from .version import ManifestVersion  # noqa: TCH001


class Flow(BaseModel):
  """Flow model. The root of the conversation description. Contains a list of conversations."""

  self_schema: HttpUrl = Field(
    alias="$schema", description="Schema URL", examples=["https://shipany.bot/schemata/v1.0/flow.json"]
  )
  name: str = Field(description="Bot name.")
  description: str = Field(description="Shortly describes the bot's purpose.")
  version: ManifestVersion = Field(
    default="1.0.0",
    description="Version of the conversation description. Supports semantic versioning.",
    examples=["1.0.0", "0.2.0-rc.1"],
  )
  conversations: list[Conversation] = Field(description="List of conversation flows supported by the bot.")
