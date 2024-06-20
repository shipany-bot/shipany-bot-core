from __future__ import annotations

import typing as t

import pytest
from pydantic import BaseModel

from shipany.bot.actions.http_request.v1 import HttpRequest
from shipany.bot.contrib.aiogram.process.http_request.v1 import process
from shipany.bot.conversation.context import conversation_context
from shipany.bot.conversation.handlers.actions import Continue

if t.TYPE_CHECKING:
  from pydantic import JsonValue
  from pytest_httpx import HTTPXMock


class MockedResponse(BaseModel):
  url: str
  status_code: int = 200
  text: str


@pytest.mark.parametrize(
  ("setup_locals", "raw_action", "captures_after", "response"),
  [
    (
      {},
      {
        "name": "HttpRequest@1",
        "url": "http://localhost:7812/get",
        "method": "GET",
        "captures": {"status_code": "response.status_code", "text": "response.text"},
        "headers": {"User-Agent": "Mozilla/5.0"},
        "query_string_parameters": {"foo": "bar"},
      },
      {"status_code": "200", "text": "unique text"},
      {
        "url": "http://localhost:7812/get?foo=bar",
        "method": "GET",
        "text": "unique text",
        "headers": {"User-Agent": "Mozilla/5.0"},
      },
    ),
    (
      {},
      {
        "name": "HttpRequest@1",
        "url": "http://localhost:7812/post",
        "method": "POST",
        "captures": {"status_code": "response.status_code", "text": "response.text"},
        "headers": {"Content-Type": "application/json"},
        "body": {"foo": "bar"},
      },
      {"status_code": "200", "text": "response text"},
      {"url": "http://localhost:7812/post", "method": "POST", "text": "response text"},
    ),
    (
      {},
      {
        "name": "HttpRequest@1",
        "url": "http://localhost:7812/post",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": {"foo": "bar"},
      },
      {},
      {"url": "http://localhost:7812/post", "method": "POST", "text": "response text"},
    ),
  ],
)
@pytest.mark.asyncio()
async def test_state_action(
  raw_action: dict[str, JsonValue],
  captures_after: dict[str, str],
  response: dict[str, JsonValue],
  httpx_mock: HTTPXMock,
) -> None:
  httpx_mock.add_response(**MockedResponse.model_validate(response).model_dump())
  with conversation_context() as ctx:
    action = HttpRequest.model_validate(raw_action)
    result = await process(ctx, action)
    match result:
      case Continue():
        assert ctx.captures == captures_after
      case _:  # pragma: no cover
        pytest.fail("Unexpected result")
