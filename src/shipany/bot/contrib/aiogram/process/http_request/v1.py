from __future__ import annotations

import json
import typing as t
from argparse import Namespace
from functools import partial

import httpx
from jinja2 import BaseLoader, Environment
from jinja2.runtime import Context as JinjaContext

from shipany.bot.contrib.aiogram.action_dispatcher import GoToNextAction

if t.TYPE_CHECKING:
  from shipany.bot.actions.http_request.v1 import HttpRequest
  from shipany.bot.contrib.aiogram.context import Context


class LazyJinjaContext(JinjaContext):
  def __init__(
    self: t.Self,
    response: httpx.Response,
    environment: Environment,
    parent: dict[str, t.Any],
    name: str | None,
    blocks: dict[str, t.Callable[[JinjaContext], t.Iterator[str]]],
    globals: t.MutableMapping[str, t.Any] | None = None,
  ) -> None:
    super().__init__(environment, parent, name, blocks, globals)

    self._response = response

  def resolve_or_missing(self: t.Self, key: str) -> t.Any:  # noqa: ANN401
    try:
      if key == "response":
        return Namespace(
          status_code=str(self._response.status_code),
          text=self._response.text,
          headers=json.dumps(self._response.headers.multi_items()),
        )
    except KeyError:
      return super().resolve_or_missing(key)


def env_from_response(response: httpx.Response) -> Environment:
  jinja_env = Environment(loader=BaseLoader(), autoescape=False)  # noqa: S701
  jinja_env.context_class = t.cast(type[JinjaContext], partial(LazyJinjaContext, response))
  return jinja_env


def template_from_response(template: str, response: httpx.Response) -> str:
  env = env_from_response(response)
  return env.from_string(template).render()


async def process(ctx: Context, action: HttpRequest) -> GoToNextAction:
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
      for key, template in action.captures.items():
        ctx.captures[key] = template_from_response("{{" + template + "}}", response)

  return GoToNextAction()
