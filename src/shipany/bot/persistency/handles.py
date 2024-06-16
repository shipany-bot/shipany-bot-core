from __future__ import annotations

import sys
import typing as t
import warnings
from abc import ABC, abstractmethod

if t.TYPE_CHECKING:
  from .scopes import Scope


class HandleGenerator(ABC):
  @abstractmethod
  def generate(self: t.Self, key: str, scope: list[Scope]) -> str:
    raise NotImplementedError


class NoScopeHandleGenerator(HandleGenerator):
  """Generates a handle for a capture given a key and a scope.

  The handle is used to store and retrieve a value from a capture. The handle should be unique
  for each key and scope.

  The implementation should be:
    - deterministic and should not depend on the environment or the state of the system
    - thread-safe
    - stateless
    - side-effect free
    - idempotent

  By default, the handle is the key itself. It simplifies testing and debugging. However, it is not
  suitable for production.

  """

  def generate(self: t.Self, key: str, _: list[Scope]) -> str:
    if "pytest" not in sys.modules:
      warnings.warn(
        "Stub implementation of CaptureKeyGenerator is activated. Do not use it in production", stacklevel=2
      )
    return key


class HandleGeneratorFactory:
  def create(self: t.Self, _: t.Any) -> HandleGenerator:  # noqa: ANN401
    return NoScopeHandleGenerator()
