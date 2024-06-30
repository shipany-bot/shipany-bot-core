from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
  from pydantic import JsonValue


class WebserverEventsDispatcher:
  async def on_startup(self: t.Self) -> None:
    raise NotImplementedError("Not implemented yet")

  async def on_updates(self: t.Self, updates: dict[str, JsonValue]) -> t.Any:  # noqa: ANN401
    raise NotImplementedError("Not implemented yet")

  async def on_shutdown(self: t.Self) -> None:
    raise NotImplementedError("Not implemented yet")
