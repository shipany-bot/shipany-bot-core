from __future__ import annotations

import logging
import typing as t
from contextlib import contextmanager

import inject
from aiogram import types as aiogram_types  # noqa: TCH002
from pydantic import BaseModel, Field

from shipany.bot.runtime.captures import CapturesProvider
from shipany.bot.runtime.secrets import SecretsProvider

logger = logging.getLogger(__name__)


class Context(BaseModel):
  captures: t.MutableMapping[str, str] = Field(default_factory=dict)
  secrets: t.Mapping[str, str] = Field(frozen=True, default_factory=dict)
  event: aiogram_types.TelegramObject


@contextmanager
def context(event: aiogram_types.TelegramObject) -> t.Iterator[Context]:
  try:
    secrets_provider = inject.instance(SecretsProvider)
  except inject.InjectorException:  # pragma: no cover
    logger.warning(
      "SecretsProvider is not found in the injector. Have you forgotten to call default_runtime_injections?"
    )
    raise

  try:
    captures_provider = inject.instance(CapturesProvider)
  except inject.InjectorException:  # pragma: no cover
    logger.warning(
      "CapturesProvider is not found in the injector. Have you forgotten to call default_runtime_injections?"
    )
    raise

  ctx = Context(captures=captures_provider.dump(), secrets=secrets_provider.dump(), event=event)

  logger.info("Context is opened with captures: %s, and secrets: %s", ctx.captures, ctx.secrets)
  yield ctx
  logger.info("Context is closed with captures: %s", ctx.captures)

  captures_provider.load(ctx.captures)
