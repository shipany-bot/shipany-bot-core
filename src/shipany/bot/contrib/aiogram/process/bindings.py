import importlib
import inspect
import logging

import inject

logger = logging.getLogger(__name__)


def _load_children_bindings(binder: inject.Binder) -> None:
  parent_module_name = ".".join(__name__.split(".")[:-1])
  parent_module = importlib.import_module(parent_module_name)
  for member in inspect.getmembers(parent_module, inspect.ismodule):
    if member[0] == "bindings":
      continue  # Skip self
    try:
      bindings_module_name = ".".join([parent_module_name, member[0], "bindings"])
      bindings = importlib.import_module(bindings_module_name)
    except ImportError:
      continue

    try:
      bindings.default_bindings(binder)
    except AttributeError:  # pragma: no cover
      logger.warning("Module '%s' does not have 'default_bindings' function", bindings_module_name)
      continue


def default_bindings(binder: inject.Binder) -> None:
  _load_children_bindings(binder)
