from __future__ import annotations

import typing as t

import httpx

from shipany.bot.conversation.handlers.actions import Continue
from shipany.bot.conversation.renders.jinja_env import value_from_context

if t.TYPE_CHECKING:
  from shipany.bot.actions.http_request.v1 import HttpRequest
  from shipany.bot.conversation.context import ConversationContext


async def process(ctx: ConversationContext, action: HttpRequest) -> Continue:
  async with httpx.AsyncClient() as client:
    response = await client.request(
      method=action.method,
      url=str(action.url),
      headers=action.headers,
      params=action.query_string_parameters,
      auth=tuple(action.basic_auth.split(":")) if action.basic_auth else None,
      json=action.body,
      timeout=action.timeout,
    )
    if action.captures:
      response_context = ctx.model_copy(update={"event": response})
      for key, value in action.captures.items():
        ctx.captures.set(key, value_from_context(value, response_context, scopes=[], safe=True), scope=[])

  return Continue()
