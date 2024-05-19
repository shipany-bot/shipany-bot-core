from __future__ import annotations

import contextlib
import json
import logging
from asyncio import run as asyncio_run
from importlib import metadata
from pathlib import Path

import httpx
import typer
from aiogram.dispatcher.dispatcher import Dispatcher
from pydantic import HttpUrl, TypeAdapter, ValidationError
from pydantic_core import Url

from shipany.bot import loader
from shipany.bot.contrib.aiogram import backend, router
from shipany.bot.conversation.models import Flow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = typer.Typer()


def dispatcher(flow: Flow) -> Dispatcher:
  dp = Dispatcher()
  dp.include_router(router.create(flow))
  return dp


@app.command()
def run(source: str = typer.Argument(help="Path or URL to the json file with the conversation description")) -> None:
  """Runs the bot with the conversation description from the given file stored locally or remotely.

  Expects BOT_TOKEN environment variables to be set.
  """
  from shipany.bot.config import bot_config

  url: HttpUrl | Path | None = None

  if url is None:
    with contextlib.suppress(ValidationError):
      url = TypeAdapter(Url).validate_python(source)

  if url is None:
    with contextlib.suppress(OSError):
      url = Path(source).resolve(strict=True)

  match url:
    case Url():
      with httpx.Client() as client:
        response = client.get(str(url))
        response.raise_for_status()
      flow = loader.load(response.text)
    case Path():
      flow = loader.load(url.read_text())
    case None:
      typer.echo("Invalid source. Please provide a valid URL or a path to the file.")
      raise typer.Exit(1)

  instance = backend.create_instance(bot_config)
  asyncio_run(dispatcher(flow).start_polling(instance))


@app.command()
def schema(
  indent: int = typer.Option(2, help="Non-negative number to pretty-print JSON with the given indent levale"),
) -> None:
  """Prints the JSON schema of the conversation description."""
  typer.echo(json.dumps(Flow.model_json_schema(), indent=indent))


@app.command()
def version() -> None:
  """Prints the version."""
  version = metadata.version("shipany-bot-core")
  typer.echo(version)


if __name__ == "__main__":
  app()
