import json
import logging
from asyncio import run as asyncio_run
from pathlib import Path

import typer
from aiogram.dispatcher.dispatcher import Dispatcher

from shipany.bot import loader
from shipany.bot.contrib.aiogram import backend, router
from shipany.bot.conversation.v1.models import Flow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = typer.Typer()


def dispatcher(flow: Flow) -> Dispatcher:
  dp = Dispatcher()
  dp.include_router(router.create(flow))
  return dp


@app.command()
def run(
  source: Path = typer.Argument(..., help="Path to the json file with the conversation description", exists=True),  # noqa: B008
) -> None:
  from shipany.bot.config import bot_config

  instance = backend.create_instance(bot_config)
  flow = loader.load(source.read_text())
  asyncio_run(dispatcher(flow).start_polling(instance))


@app.command()
def schema(
  indent: int = typer.Option(2, help="Non-negative number to pretty-print JSON with the given indent levale"),
) -> None:
  typer.echo(json.dumps(Flow.model_json_schema(), indent=indent))


if __name__ == "__main__":
  app()
