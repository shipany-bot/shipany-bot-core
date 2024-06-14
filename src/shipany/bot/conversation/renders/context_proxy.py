import typing as t

from shipany.bot.conversation.context import ConversationContext
from shipany.bot.jsonlogic import SupportsGetOrDefault

from .jinja_env import template_from_context


def proxy(ctx: ConversationContext) -> SupportsGetOrDefault:
  class _Proxy:
    def __getitem__(self: t.Self, key: str) -> str:
      return template_from_context("{{" + key + "}}", ctx, safe=False)

  return _Proxy()
