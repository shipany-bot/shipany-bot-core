from __future__ import annotations

from typing import Mapping, MutableMapping

from aiogram import types as aiogram_types
from pydantic import BaseModel, Field


def _collect_secrets() -> Mapping[str, str]:
  return {"openai_token": "t0k3n"}


class Context(BaseModel):
  captures: MutableMapping[str, str] = Field(default_factory=dict)
  secrets: Mapping[str, str] = Field(frozen=True, default_factory=_collect_secrets)
  event: aiogram_types.TelegramObject


persistent_context = Context(event=aiogram_types.TelegramObject())
