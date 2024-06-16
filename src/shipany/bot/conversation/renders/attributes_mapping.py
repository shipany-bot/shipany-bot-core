from __future__ import annotations

import logging
import typing as t
from collections.abc import Mapping

import inject

from shipany.bot.conversation.context import ConversationContext

if t.TYPE_CHECKING:
  from shipany.bot.persistency.scopes import Scope

logger = logging.getLogger(__name__)


class VariablesGetter(Mapping[str, t.Any]):
  def __init__(self: t.Self, ctx: ConversationContext, captures_scopes: list[Scope], *, safe: bool) -> None:
    self._ctx = ctx
    self._captures_scopes = captures_scopes
    self._safe = safe

  def __getitem__(self: t.Self, key: str) -> t.Any:  # noqa: ANN401
    logger.info("Getting the attribute '%s'", key)

    try:
      proxy = t.cast(t.Callable[[ConversationContext], t.Any], inject.instance(key))
      return proxy(self._ctx)
    except inject.InjectorException:  # pragma: no cover
      pass

    if key == "secrets":
      return self._ctx.runtime.secrets if self._safe else {key: "*****" for key in self._ctx.runtime.secrets}

    if value := self._ctx.captures.get(key, scope=self._captures_scopes):
      return value

    raise KeyError(key)

  def __iter__(self: t.Self) -> t.Iterator[str]:
    raise NotImplementedError

  def __len__(self: t.Self) -> int:
    raise NotImplementedError
