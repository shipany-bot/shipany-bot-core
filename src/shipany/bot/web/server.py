from __future__ import annotations

import typing as t

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from pydantic import BaseModel, ConfigDict, Field

if t.TYPE_CHECKING:
  from shipany.bot.config import BotConfig
  from shipany.bot.conversation.models.v1.flow import Flow

app = FastAPI()


@app.get("/")
async def root() -> str:
  return "Hello, world!"


async def current_bot_flow() -> Flow:
  raise RuntimeError("Dependency is not overridden")


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


async def _hook_endpoint(
  request: Request,
  flow: t.Annotated[Flow, Depends(current_bot_flow)],
) -> WebhookResponse:
  for webhook in flow.webhooks:
    if webhook.path == request.url.path and webhook.method == request.method:
      break
  else:
    raise NotImplementedError("Not implemented")

  try:
    _check_expectations(request.headers, webhook.expect.headers, "header")
    _check_expectations(request.query_params, webhook.expect.query_params, "query parameter")
  except HTTPException as e:
    e.status_code = webhook.status_code_error
    raise e from None

  return WebhookResponse(message="OK")


def serve(flow: Flow, bot_config: BotConfig) -> t.Coroutine[t.Any, t.Any, None]:
  for webhook in flow.webhooks:
    app.add_api_route(
      webhook.path,
      endpoint=t.cast(t.Callable[..., t.Coroutine[t.Any, t.Any, Response]], _hook_endpoint),
      dependencies=[],
      methods=[webhook.method],
      status_code=webhook.status_code_ok,
      response_model_exclude_none=True,
    )
  app.dependency_overrides[current_bot_flow] = lambda: flow

  config = uvicorn.Config(
    app,
    host=bot_config.web_server_host,
    port=bot_config.web_server_port,
    loop="asyncio",
  )
  server = uvicorn.Server(config)
  return server.serve()
