import typing as t

from shipany.bot.contrib.aiogram.context import BotContext
from shipany.bot.jsonlogic import SupportsGetOrDefault

from .jinja_env import template_from_context


def proxy(ctx: BotContext) -> SupportsGetOrDefault:
  class _Proxy:
    def __getitem__(self: t.Self, key: str) -> str:
      return template_from_context("{{" + key + "}}", ctx)

  return _Proxy()
