from __future__ import annotations

import logging
import typing as t
from contextlib import contextmanager

import inject
from aiogram import types as aiogram_types  # noqa: TCH002
from pydantic import BaseModel, ConfigDict, Field

from shipany.bot.providers.captures import CapturesModifier, CapturesProvider
from shipany.bot.runtime.context import RuntimeContext, runtime_context

logger = logging.getLogger(__name__)

__all__ = ["bot_context", "BotContext"]


class BotContext(BaseModel):
  runtime: RuntimeContext = Field(..., description="Runtime context.")
  captures: CapturesModifier = Field(..., description="Captures modifier.")
  event: aiogram_types.TelegramObject = Field(..., description="Telegram event like message, callback_query, etc.")

  model_config = ConfigDict(extra="forbid", frozen=True, arbitrary_types_allowed=True)


@contextmanager
def bot_context(event: aiogram_types.TelegramObject) -> t.Iterator[BotContext]:
  captures_provider: CapturesProvider | None = None
  try:
    captures_provider = inject.instance(CapturesProvider)
  except inject.InjectorException:  # pragma: no cover
    logger.warning(
      "CapturesProvider is not found in the injector. Have you forgotten to call default_runtime_bindings?"
    )
    raise

  with runtime_context() as runtime, captures_provider.snapshot() as captures:
    ctx = BotContext(captures=captures, runtime=runtime, event=event)
    yield ctx
