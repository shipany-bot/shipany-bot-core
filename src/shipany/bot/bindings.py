import inject

from shipany.bot.contrib.aiogram import bindings as aiogram_bindings
from shipany.bot.providers import bindings as providers_bindings


def default_bindings(binder: inject.Binder) -> None:
  providers_bindings.default_bindings(binder)
  aiogram_bindings.default_bindings(binder)
