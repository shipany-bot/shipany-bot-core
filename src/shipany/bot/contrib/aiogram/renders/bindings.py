import inject

from . import namespaces


def default_bindings(binder: inject.Binder) -> None:
  binder.bind("message", namespaces.message_namespace)
  binder.bind("user", namespaces.user_namespace)
  binder.bind("reaction", namespaces.reaction_namespace)
