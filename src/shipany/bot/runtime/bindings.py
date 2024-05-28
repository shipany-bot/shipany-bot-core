import inject

from shipany.bot.runtime.captures import CapturesProvider, InMemoryCapturesProvider
from shipany.bot.runtime.secrets import SecretsProvider, StubSecretsProvider


def default_runtime_injections(binder: inject.Binder) -> None:
  binder.bind(CapturesProvider, InMemoryCapturesProvider())
  binder.bind(SecretsProvider, StubSecretsProvider())
