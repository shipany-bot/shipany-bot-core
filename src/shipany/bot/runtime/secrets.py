import typing as t
from abc import ABC, abstractmethod


class SecretsProvider(ABC):
  @abstractmethod
  def dump(self: t.Self) -> t.Mapping[str, str]:
    raise NotImplementedError


class StubSecretsProvider:
  def dump(self: t.Self) -> t.Mapping[str, str]:
    return {}
