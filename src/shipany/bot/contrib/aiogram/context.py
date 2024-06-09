from __future__ import annotations

import logging
import typing as t
from contextlib import contextmanager

from aiogram import types as aiogram_types  # noqa: TCH002
from pydantic import Field

from shipany.bot.runtime.context import Context, context as parent_context

logger = logging.getLogger(__name__)

__all__ = ["context", "ExtendedContext"]


class ExtendedContext(Context):
  event: aiogram_types.TelegramObject = Field(..., description="Telegram event like message, callback_query, etc.")


@contextmanager
def context(event: aiogram_types.TelegramObject) -> t.Iterator[ExtendedContext]:
  with parent_context() as parent:
    yield ExtendedContext(**parent.model_dump(), event=event)
