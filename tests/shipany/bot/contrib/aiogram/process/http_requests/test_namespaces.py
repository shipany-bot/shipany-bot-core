from __future__ import annotations

from shipany.bot.contrib.aiogram.process.http_request.namespaces import response_namespace
from shipany.bot.conversation.context import conversation_context


async def test_another_event() -> None:
  async with conversation_context() as ctx:
    assert response_namespace(ctx) is None
