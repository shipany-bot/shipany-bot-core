import inject

from .process import bindings as process_bindings
from .renders import bindings as renders_bindings


def default_bindings(binder: inject.Binder) -> None:
  process_bindings.default_bindings(binder)
  renders_bindings.default_bindings(binder)
