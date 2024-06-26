import typing as t
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def _override_bot_config(monkeypatch: pytest.MonkeyPatch) -> t.Generator[None, t.Any, None]:
  # import environment variables from test.environment file to override any existing ones

  with monkeypatch.context() as m:
    m.setenv("BOT_TOKEN", "1231243:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
    m.setenv("TELEGRAM_API_URL", "http://localhost:8081")
    m.setenv("TELEGRAM_WEBHOOK_URL", "http://localhost:8088/webhook")
    m.setenv("WEB_BOT_WEBHOOK_SECRET", "")
    yield


@pytest.fixture()
def flows_path_factory() -> t.Callable[[int], Path]:
  def func(version: int) -> Path:
    directory = Path(__file__).parent / Path(f"fixtures/payloads/schema/v{version}")
    if not directory.exists():  # pragma: no cover
      raise FileNotFoundError(f"Directory {directory} does not exist. Can't find payloads for version {version}")
    return directory

  return func
