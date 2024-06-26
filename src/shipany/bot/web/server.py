from __future__ import annotations

import json
import logging
import typing as t
from contextlib import asynccontextmanager

import inject
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from starlette import status

from shipany.bot.config import BotConfig
from shipany.bot.contrib.aiogram.factories import telegram_objects
from shipany.bot.conversation import errors
from shipany.bot.conversation.context import conversation_context
from shipany.bot.conversation.handlers.activations import ActivationHandler
from shipany.bot.conversation.models import Conversation, Flow, WebhookActivation
from shipany.bot.web.events import WebserverEventsDispatcher

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> t.AsyncIterator[None]:
  await inject.instance(WebserverEventsDispatcher).on_startup()
  yield
  await inject.instance(WebserverEventsDispatcher).on_shutdown()


app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None)


@app.get("/", response_class=HTMLResponse)
async def root() -> str:
  about_me = await telegram_objects.bot().me()
  return f"""\
<!DOCTYPE html>
<html>
<head>
<title>{about_me.first_name}</title>
</head>
<body>
<h1>{about_me.first_name}</h1>
<p>Hi, I am @{about_me.username}.</p>
<p>Talk to me at <a href="https://t.me/{about_me.username}">t.me/{about_me.username}</a>.</p>
</body>
</html>"""


async def current_bot_flow() -> Flow:
  raise NotImplementedError("Dependency is not overridden")


class WebhookResponse(BaseModel):
  message: str = Field(..., description="Response message")
  model_config = ConfigDict()


def _check_expectations(
  inputs: t.Mapping[str, str], expectations: t.Mapping[str, str], expected_type: t.Literal["header", "query parameter"]
) -> None:
  for attr, value in expectations.items():
    if value != inputs.get(attr):
      raise HTTPException(
        detail=f"The request did not meet expectations. Check {expected_type} '{attr}'.", status_code=400
      )


def _find_webhook_activation(
  flow: Flow, path: str, method: str
) -> t.Generator[tuple[WebhookActivation, Conversation], None, None]:
  for conversation in flow.conversations:
    for activation in conversation.activations:
      if (
        isinstance(activation, WebhookActivation)
        and activation.webhook.path == path
        and activation.webhook.method == method
      ):
        yield activation, conversation


async def _feed_endpoint(request: Request) -> Response:
  try:
    updates = await request.json()
  except json.JSONDecodeError:
    return Response(status_code=status.HTTP_400_BAD_REQUEST, content="Expecting JSON payload.")

  try:
    response = await inject.instance(WebserverEventsDispatcher).on_updates(updates)
  except ValidationError:
    return Response(status_code=status.HTTP_400_BAD_REQUEST, content="Invalid JSON payload.")

  if response is not None:
    logger.warning("Unprocessed response from the dispatcher: %s", response)
  return Response(status_code=status.HTTP_204_NO_CONTENT)


async def _hook_endpoint(
  request: Request,
  flow: t.Annotated[Flow, Depends(current_bot_flow)],
) -> WebhookResponse:
  try:
    activation, conversation = next(_find_webhook_activation(flow, request.url.path, request.method))
  except StopIteration:  # pragma: no cover
    raise HTTPException(detail="Webhook handler not found", status_code=404) from None

  webhook = activation.webhook

  try:
    _check_expectations(request.headers, webhook.expect.headers, "header")
    _check_expectations(request.query_params, webhook.expect.query_params, "query parameter")
  except HTTPException as e:
    e.status_code = webhook.status_code_error
    raise e from None

  async with conversation_context() as ctx:
    try:
      handler = ActivationHandler(ctx, activation)
      await handler(conversation.steps)
    except errors.ActivationPreconditionNotMeetError:
      logger.info("The condition is not met. Skipping the handler.")
      return WebhookResponse(message="The condition is not met. Skipping the handler.")

  return WebhookResponse(message="OK")


def add_webhooks(flow: Flow) -> None:
  for conversation in flow.conversations:
    for activation in conversation.activations:
      match activation:
        case WebhookActivation(webhook=webhook):
          app.add_api_route(
            webhook.path,
            endpoint=t.cast(t.Callable[..., t.Coroutine[t.Any, t.Any, Response]], _hook_endpoint),
            methods=[webhook.method],
            status_code=webhook.status_code_ok,
            response_model_exclude_none=True,
          )
        case _:
          logger.warning("Unsupported activation type in context of Web server: %s", type(activation))
  app.dependency_overrides[current_bot_flow] = lambda: flow


def secret_in_headers(request: Request) -> None:
  bot_config = BotConfig()

  secret = bot_config.web_bot_webhook_secret.get_secret_value()
  if secret != request.headers.get("x-telegram-bot-api-secret-token", ""):
    raise HTTPException(detail="Secret is invalid", status_code=status.HTTP_403_FORBIDDEN)


def add_bot_webhook(path: str) -> None:
  logger.info("Adding bot webhook path: %s", path)
  app.add_api_route(path, endpoint=_feed_endpoint, methods=["POST"], dependencies=[Depends(secret_in_headers)])


def serve(flow: Flow, bot_config: BotConfig) -> t.Coroutine[t.Any, t.Any, None]:
  add_webhooks(flow)
  if bot_config.web_bot_webhook_path:
    add_bot_webhook(bot_config.web_bot_webhook_path)

  config = uvicorn.Config(
    app,
    host=bot_config.web_server_host,
    port=bot_config.web_server_port,
    loop="asyncio",
  )
  server = uvicorn.Server(config)
  return server.serve()
