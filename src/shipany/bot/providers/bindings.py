import inject

from .captures import CapturesProvider, InMemoryCapturesProvider
from .secrets import SecretsProvider, StubSecretsProvider


def default_bindings(binder: inject.Binder) -> None:
  binder.bind(CapturesProvider, InMemoryCapturesProvider())
  binder.bind(SecretsProvider, StubSecretsProvider())
