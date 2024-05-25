from __future__ import annotations

import logging
import typing as t

import inject
from aiogram import types as aiogram_types
from pydantic import BaseModel, Field

from shipany.bot.runtime.secrets import SecretsProvider

logger = logging.getLogger(__name__)


def _collect_secrets() -> t.Mapping[str, str]:
  try:
    instance = t.cast(SecretsProvider, inject.instance(SecretsProvider))
    return instance.dump()
  except inject.InjectorException:
    logger.warning("No secrets are configured.")
    return {}


class Context(BaseModel):
  captures: t.MutableMapping[str, str] = Field(default_factory=dict)
  secrets: t.Mapping[str, str] = Field(frozen=True, default_factory=_collect_secrets)
  event: aiogram_types.TelegramObject


persistent_context = Context(event=aiogram_types.TelegramObject())
