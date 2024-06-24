from __future__ import annotations

import typing as t
from contextlib import asynccontextmanager


class SecretsProvider:
  @asynccontextmanager
  async def snapshot(self: t.Self) -> t.AsyncIterator[t.Mapping[str, str]]:
    raise NotImplementedError
    yield {}  # tweak to make mypy happy


class StubSecretsProvider:
  def __init__(self: t.Self, initial_value: t.Mapping[str, str] | None = None) -> None:
    self._secrets = initial_value if initial_value is not None else {}

  @asynccontextmanager
  async def snapshot(self: t.Self) -> t.AsyncIterator[t.Mapping[str, str]]:
    yield self._secrets
