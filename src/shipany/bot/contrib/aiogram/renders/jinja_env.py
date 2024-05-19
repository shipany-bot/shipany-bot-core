from __future__ import annotations

import typing as t
from functools import partial

from jinja2 import BaseLoader, Environment
from jinja2.runtime import Context as JinjaContext

from .attributes_mapping import VariablesGetter

if t.TYPE_CHECKING:
  from shipany.bot.contrib.aiogram.context import Context


class LazyJinjaContext(JinjaContext):
  def __init__(
    self: t.Self,
    getter: VariablesGetter,
    environment: Environment,
    parent: dict[str, t.Any],
    name: str | None,
    blocks: dict[str, t.Callable[[JinjaContext], t.Iterator[str]]],
    globals: t.MutableMapping[str, t.Any] | None = None,
  ) -> None:
    super().__init__(environment, parent, name, blocks, globals)

    self._getter = getter

  def resolve_or_missing(self: t.Self, key: str) -> t.Any:  # noqa: ANN401
    try:
      return self._getter[key]
    except KeyError:
      return super().resolve_or_missing(key)


def _jinja_context_from(ctx: Context) -> type[JinjaContext]:
  return t.cast(type[JinjaContext], partial(LazyJinjaContext, VariablesGetter(ctx)))


def render_in_context(ctx: Context) -> Environment:
  jinja_env = Environment(loader=BaseLoader(), autoescape=False)  # noqa: S701
  jinja_env.context_class = _jinja_context_from(ctx)
  return jinja_env


def template_from_context(template: str, ctx: Context) -> str:
  env = render_in_context(ctx)
  return env.from_string(template).render()
