from pathlib import Path
from typing import Callable

import pytest
from dotenv import load_dotenv

# import environment variables from test.environment file to override any existing ones
if not load_dotenv(Path(__file__).parent / "fixtures/test.env", override=True):
  raise FileNotFoundError("No test.env file found in fixtures directory")

# make sure that the environment variables are loaded before importing the settings
from shipany.bot import bot_config  # noqa: F401


@pytest.fixture()
def flows_path_factory() -> Callable[[int], Path]:
  def func(version: int) -> Path:
    directory = Path(__file__).parent / Path(f"fixtures/payloads/schema/v{version}")
    if not directory.exists():
      raise FileNotFoundError(f"Directory {directory} does not exist. Can't find payloads for version {version}")
    return directory

  return func
