from __future__ import annotations

import typing as t
from contextlib import contextmanager


class CapturesProvider:
  @contextmanager
  def snapshot(self: t.Self) -> t.Iterator[CapturesModifier]:
    raise NotImplementedError


class CapturesModifier:
  def __init__(self: t.Self, captures: t.MutableMapping[str, str]) -> None:
    self._captures = captures

  def __setitem__(self: t.Self, key: str, value: str) -> None:
    self._captures[key] = value

  def __getitem__(self: t.Self, key: str) -> t.Any:  # noqa: ANN401
    return self._captures[key]

  def __contains__(self: t.Self, key: str) -> bool:
    return key in self._captures

  def __iter__(self: t.Self) -> t.Iterator[str]:
    yield from self._captures

  def __eq__(self: t.Self, other: t.Any) -> bool:  # noqa: ANN401
    return self._captures == other._captures if isinstance(other, CapturesModifier) else self._captures == other

  def __len__(self: t.Self) -> int:
    return len(self._captures)

  def __delitem__(self: t.Self, key: str) -> None:
    del self._captures[key]


class InMemoryCapturesProvider:
  def __init__(self: t.Self, *, initial_value: t.Mapping[str, str] | None = None) -> None:
    self._captures: dict[str, str] = dict(**initial_value) if initial_value else {}

  @contextmanager
  def snapshot(self: t.Self) -> t.Iterator[CapturesModifier]:
    yield CapturesModifier(self._captures)
