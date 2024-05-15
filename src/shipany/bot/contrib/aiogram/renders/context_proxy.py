from typing_extensions import Self

from shipany.bot.contrib.aiogram.context import Context
from shipany.bot.jsonlogic import SupportsGetOrDefault

from .jinja_env import template_from_context


def proxy(ctx: Context) -> SupportsGetOrDefault:
  class _Proxy:
    def __getitem__(self: Self, key: str) -> str:
      return template_from_context("{{" + key + "}}", ctx)

  return _Proxy()
