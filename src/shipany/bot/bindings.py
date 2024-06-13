import inject

from shipany.bot.providers.captures import CapturesProvider, InMemoryCapturesProvider
from shipany.bot.providers.secrets import SecretsProvider, StubSecretsProvider


def default_runtime_bindings(binder: inject.Binder) -> None:
  binder.bind(CapturesProvider, InMemoryCapturesProvider())
  binder.bind(SecretsProvider, StubSecretsProvider())
