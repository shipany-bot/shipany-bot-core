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
  def __init__(
    self: t.Self,
    captures: t.MutableMapping[str, str],
    locals: t.MutableMapping[str, str],
    handle_generator: HandleGenerator,
  ) -> None:
    self._captures = captures
    self._locals = locals
    self._handle_generator = handle_generator

  @_validate_call
  def set(self, key: str, value: str, *, scope: list[Scope]) -> None:  # noqa: ANN101
    if not scope:
      self._locals[key] = value
    self._captures[self._key(key, scope)] = value

  @_validate_call
  def get(self, key: str, *, scope: list[Scope]) -> str | None:  # noqa: ANN101
    if not scope:
      return self._locals[key]
    return self._captures[self._key(key, scope)]

  @_validate_call
  def remove(self, key: str, *, scope: list[Scope]) -> None:  # noqa: ANN101
    if not scope:
      del self._locals[key]
    del self._captures[self._key(key, scope)]

  def _key(self: t.Self, key: str, scope: list[Scope]) -> str:
    handle = self._handle_generator.generate(key, scope)
    logger.info("Generated handle for key=%s and scope=%s: %s", key, scope, handle)
    return handle

  def __eq__(self: t.Self, other: t.Any) -> bool:  # noqa: ANN401
    if not isinstance(other, CapturesModifier):
      return other == dict(self._captures) | dict(self._locals)
    return self._captures == other


class InMemoryCapturesProvider:
  def __init__(
    self: t.Self,
    *,
    setup_captures: t.Mapping[str, str] | None = None,
    setup_locals: t.Mapping[str, str] | None = None,
  ) -> None:
    self._locals: dict[str, str] = dict(**setup_locals) if setup_locals else {}
    self._captures: dict[str, str] = dict(**setup_captures) if setup_captures else {}

  @contextmanager
  def snapshot(self: t.Self, handle_generator: HandleGenerator) -> t.Iterator[CapturesModifier]:
    yield CapturesModifier(self._captures, self._locals, handle_generator)
