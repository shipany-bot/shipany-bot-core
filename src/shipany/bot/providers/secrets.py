from __future__ import annotations

import typing as t
from contextlib import contextmanager


class SecretsProvider:
  @contextmanager
  def snapshot(self: t.Self) -> t.Iterator[t.Mapping[str, str]]:
    raise NotImplementedError


class StubSecretsProvider:
  def __init__(self: t.Self, initial_value: t.Mapping[str, str] | None = None) -> None:
    self._secrets = initial_value if initial_value is not None else {}

  @contextmanager
  def snapshot(self: t.Self) -> t.Iterator[t.Mapping[str, str]]:
    yield self._secrets
