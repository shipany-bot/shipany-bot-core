from __future__ import annotations

import logging
import typing as t
from contextlib import contextmanager

import inject
from pydantic import BaseModel, ConfigDict, Field

from shipany.bot.persistency.handles import HandleGeneratorFactory
from shipany.bot.providers.captures import CapturesModifier, CapturesProvider
from shipany.bot.runtime.context import RuntimeContext, runtime_context

logger = logging.getLogger(__name__)

__all__ = ["conversation_context", "ConversationContext"]


class ConversationContext(BaseModel):
  runtime: RuntimeContext = Field(..., description="Runtime context.")
  captures: CapturesModifier = Field(..., description="Captures modifier.")
  event: t.Any = Field(..., description="Telegram event like message, callback_query, etc.")

  model_config = ConfigDict(extra="forbid", frozen=True, arbitrary_types_allowed=True)


@contextmanager
def conversation_context(event: t.Any = None) -> t.Iterator[ConversationContext]:  # noqa: ANN401
  captures_provider: CapturesProvider | None = None
  try:
    captures_provider = inject.instance(CapturesProvider)
  except inject.InjectorException:  # pragma: no cover
    logger.warning(
      "CapturesProvider is not found in the injector. Have you forgotten to call default_runtime_bindings?"
    )
    raise

  try:
    handle_generator_factory = inject.instance(HandleGeneratorFactory)
    handle_generator = handle_generator_factory.create(event)
  except inject.InjectorException:  # pragma: no cover
    logger.warning(
      "HandleGeneratorFactory is not found in the injector. Have you forgotten to call default_runtime_bindings?"
    )
    raise

  with runtime_context() as runtime, captures_provider.snapshot(handle_generator) as captures:
    yield ConversationContext(captures=captures, runtime=runtime, event=event)
