from __future__ import annotations

from aiogram import types as aiogram_types
from pydantic import BaseModel, Field


class Context(BaseModel):
  captures: dict[str, str] = Field(default_factory=dict)
  event: aiogram_types.TelegramObject


persistent_context = Context(event=aiogram_types.TelegramObject())
