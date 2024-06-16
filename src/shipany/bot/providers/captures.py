from __future__ import annotations

import logging
import typing as t
from contextlib import contextmanager

from pydantic import ConfigDict, validate_call

from shipany.bot.persistency.scopes import Scope  # noqa: TCH001

if t.TYPE_CHECKING:
  from shipany.bot.persistency.handles import HandleGenerator

logger = logging.getLogger(__name__)


class CapturesProvider:
  @contextmanager
  def snapshot(self: t.Self, handle_generator: HandleGenerator) -> t.Iterator[CapturesModifier]:
    raise NotImplementedError


_validate_call = validate_call(config=ConfigDict(arbitrary_types_allowed=True), validate_return=True)


class CapturesModifier:
  def __init__(self: t.Self, captures: t.MutableMapping[str, str], handle_generator: HandleGenerator) -> None:
    self._captures = captures
    self._handle_generator = handle_generator

  @_validate_call
  def set(self, key: str, value: str, *, scope: list[Scope]) -> None:  # noqa: ANN101
    self._captures[self._key(key, scope)] = value

  @_validate_call
  def get(self, key: str, *, scope: list[Scope]) -> str | None:  # noqa: ANN101
    return self._captures[self._key(key, scope)]

  @_validate_call
  def remove(self, key: str, *, scope: list[Scope]) -> None:  # noqa: ANN101
    del self._captures[self._key(key, scope)]

  def _key(self: t.Self, key: str, scope: list[Scope]) -> str:
    handle = self._handle_generator.generate(key, scope)
    logger.info("Generated handle for key=%s and scope=%s: %s", key, scope, handle)
    return handle

  def __eq__(self: t.Self, other: t.Any) -> bool:  # noqa: ANN401
    return self._captures == other._captures if isinstance(other, CapturesModifier) else self._captures == other


class InMemoryCapturesProvider:
  def __init__(self: t.Self, *, initial_value: t.Mapping[str, str] | None = None) -> None:
    self._captures: dict[str, str] = dict(**initial_value) if initial_value else {}

  @contextmanager
  def snapshot(self: t.Self, handle_generator: HandleGenerator) -> t.Iterator[CapturesModifier]:
    yield CapturesModifier(self._captures, handle_generator)
