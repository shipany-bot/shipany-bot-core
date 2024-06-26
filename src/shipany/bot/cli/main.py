from __future__ import annotations

import asyncio
import contextlib
import json
import logging
import typing as t
from importlib import metadata
from pathlib import Path

import httpx
import inject
import typer
from pydantic import HttpUrl, TypeAdapter, ValidationError
from pydantic_core import Url

from shipany.bot import loader
from shipany.bot.bindings import default_bindings
from shipany.bot.config import BotConfig
from shipany.bot.conversation.models import Flow
from shipany.bot.providers.secrets import SecretsProvider
from shipany.bot.web import server

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = typer.Typer()


def captures() -> t.MutableMapping[str, str]:
  return {}


@app.command()
def run(  # noqa: C901
  source: str = typer.Argument(help="Path or URL to the json file with the conversation description"),
  backend_to_use: t.Annotated[str, typer.Option("--backend", help="Backend to use for the bot")] = "aiogram",
  secret: list[str] = typer.Option([], help="Secret in form of key=value to pass to the bot. Can be many"),  # noqa: B008
  web: bool = typer.Option(True, help="Enable the web server"),
) -> None:
  """Runs the bot with the conversation description from the given file stored locally or remotely.

  Expects BOT_TOKEN environment variables to be set.
  """
  bot_config = BotConfig()

  url: HttpUrl | Path | None = None

  if url is None:
    with contextlib.suppress(ValidationError):
      url = TypeAdapter(Url).validate_python(source)

  if url is None:
    with contextlib.suppress(OSError):
      url = Path(source).resolve(strict=True)

  if not web and bot_config.telegram_webhook_url:
    typer.echo("Web server is required for the webhook mode. Use --web flag to enable it.")
    raise typer.Exit(1)

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

  def configure_injections(binder: inject.Binder) -> None:
    default_bindings(binder)

    if secret:

      class SimpleDictAsSecretsProvider:
        def dump(self: t.Self) -> dict[str, str]:
          return dict(key_value.split("=", maxsplit=1) for key_value in secret)

      binder.bind(SecretsProvider, SimpleDictAsSecretsProvider())

  inject.configure(configure_injections)

  match backend_to_use:
    case "aiogram":
      from shipany.bot.contrib.aiogram import backend

      bot_server = backend.serve(flow)
    case _:
      typer.echo(f"Invalid backend: {backend_to_use}. Please provide a supported backend.")
      raise typer.Exit(1)

  web_server = server.serve(flow, bot_config) if web else None

  async def _run_servers() -> None:
    async with asyncio.TaskGroup() as tg:
      tg.create_task(bot_server)
      if web_server:
        tg.create_task(web_server)

  asyncio.run(_run_servers())


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
