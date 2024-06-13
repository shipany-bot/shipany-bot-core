from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod


class CapturesProvider(ABC):
  @abstractmethod
  def dump(self: t.Self) -> t.MutableMapping[str, str]:
    raise NotImplementedError

  @abstractmethod
  def load(self: t.Self, captures: t.MutableMapping[str, str]) -> None:
    raise NotImplementedError


class InMemoryCapturesProvider(CapturesProvider):
  def __init__(self: t.Self) -> None:
    self._captures: dict[str, str] = {}

  def dump(self: t.Self) -> t.MutableMapping[str, str]:
    return self._captures

  def load(self: t.Self, captures: t.MutableMapping[str, str]) -> None:
    self._captures = dict(**captures)
