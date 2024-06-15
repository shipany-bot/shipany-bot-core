from __future__ import annotations

import typing as t
from functools import partial

from jinja2 import BaseLoader, Environment
from jinja2.runtime import Context as JinjaContext

from shipany.bot.conversation.renders.attributes_mapping import VariablesGetter

if t.TYPE_CHECKING:
  from shipany.bot.conversation.context import ConversationContext


class LazyJinjaContext(JinjaContext):
  def __init__(
    self: t.Self,
    getter: t.Mapping[str, t.Any],
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


def _jinja_context_from(ctx: ConversationContext, *, safe: bool) -> type[JinjaContext]:
  return t.cast(type[JinjaContext], partial(LazyJinjaContext, VariablesGetter(ctx, safe=safe)))


def render_in_context(ctx: ConversationContext, *, safe: bool) -> Environment:
  jinja_env = Environment(loader=BaseLoader(), autoescape=False)  # noqa: S701
  jinja_env.context_class = _jinja_context_from(ctx, safe=safe)
  return jinja_env


def template_from_context(template: str, ctx: ConversationContext, *, safe: bool) -> str:
  env = render_in_context(ctx, safe=safe)
  return env.from_string(template).render()
