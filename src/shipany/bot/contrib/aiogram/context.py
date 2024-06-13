from __future__ import annotations

import logging
import typing as t
from contextlib import contextmanager

import inject
from aiogram import types as aiogram_types  # noqa: TCH002
from pydantic import BaseModel, ConfigDict, Field

from shipany.bot.providers.captures import CapturesProvider
from shipany.bot.runtime.context import RuntimeContext, runtime_context

logger = logging.getLogger(__name__)

__all__ = ["bot_context", "BotContext"]


class BotContext(BaseModel):
  runtime: RuntimeContext = Field(..., description="Runtime context.")
  captures: t.MutableMapping[str, str] = Field(default_factory=dict)
  event: aiogram_types.TelegramObject = Field(..., description="Telegram event like message, callback_query, etc.")

  model_config = ConfigDict(extra="forbid", frozen=True)


@contextmanager
def bot_context(
  event: aiogram_types.TelegramObject, *, captures: t.MutableMapping[str, str] | None = None
) -> t.Iterator[BotContext]:
  captures_provider: CapturesProvider | None = None
  try:
    if captures is None:
      captures_provider = inject.instance(CapturesProvider)
      captures = captures_provider.dump()
  except inject.InjectorException:  # pragma: no cover
    logger.warning(
      "CapturesProvider is not found in the injector. Have you forgotten to call default_runtime_bindings?"
    )
    raise

  with runtime_context() as runtime:
    ctx = BotContext(captures=captures, runtime=runtime, event=event)
    yield ctx

  if captures_provider is not None:
    captures_provider.load(ctx.captures)
