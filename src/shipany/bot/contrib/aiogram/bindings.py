import inject

from .renders import bindings


def default_bindings(binder: inject.Binder) -> None:
  bindings.default_bindings(binder)
