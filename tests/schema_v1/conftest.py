from pathlib import Path
from typing import Callable

import pytest


@pytest.fixture()
def flows_path(flows_path_factory: Callable[[int], Path]) -> Path:
  return flows_path_factory(1)
