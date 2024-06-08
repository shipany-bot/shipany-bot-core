import typing as t

import uvicorn
from fastapi import FastAPI

from shipany.bot.config import BotConfig
from shipany.bot.conversation.models.v1.flow import Flow

app = FastAPI()


@app.get("/")
async def root() -> str:
  return "Hello, world!"


def serve(flow: Flow, bot_config: BotConfig) -> t.Coroutine[t.Any, t.Any, None]:
  config = uvicorn.Config(
    app,
    host=bot_config.web_server_host,
    port=bot_config.web_server_port,
    loop="asyncio",
  )
  server = uvicorn.Server(config)
  return server.serve()
