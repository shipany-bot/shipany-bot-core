import inject

from . import namespaces


def default_bindings(binder: inject.Binder) -> None:
  binder.bind("response", namespaces.response_namespace)
