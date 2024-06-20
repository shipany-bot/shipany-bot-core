import inject

from shipany.bot.persistency.handles import HandleGeneratorFactory

from . import handles


def default_bindings(binder: inject.Binder) -> None:
  binder.bind(HandleGeneratorFactory, handles.HandleGeneratorFactory())
