import inject

from .process.http_request import bindings as http_request_bindings
from .renders import bindings


def default_bindings(binder: inject.Binder) -> None:
  bindings.default_bindings(binder)
  http_request_bindings.default_bindings(binder)
