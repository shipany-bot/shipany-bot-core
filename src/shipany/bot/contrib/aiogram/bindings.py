import inject

from .persistency import bindings as persistency_bindings
from .process import bindings as process_bindings
from .renders import bindings as renders_bindings


def default_bindings(binder: inject.Binder) -> None:
  process_bindings.default_bindings(binder)
  renders_bindings.default_bindings(binder)
  persistency_bindings.default_bindings(binder)
