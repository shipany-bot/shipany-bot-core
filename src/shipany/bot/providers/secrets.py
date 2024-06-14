import typing as t
from contextlib import contextmanager


class SecretsProvider:
  @contextmanager
  def snapshot(self: t.Self) -> t.Iterator[t.Mapping[str, str]]:
    raise NotImplementedError


class StubSecretsProvider:
  @contextmanager
  def snapshot(self: t.Self) -> t.Iterator[t.Mapping[str, str]]:
    yield {}
