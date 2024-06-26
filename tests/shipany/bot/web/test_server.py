import typing as t

import pytest
from aiogram.types import User
from fastapi.testclient import TestClient

from shipany.bot.contrib.aiogram.factories import telegram_objects
from shipany.bot.conversation.loader import load
from shipany.bot.web.server import add_bot_webhook, add_webhooks, app


def test_root(monkeypatch: pytest.MonkeyPatch) -> None:
  class MockBot:
    async def me(self: t.Self) -> User:
      return User(id=1, is_bot=True, first_name="Test", username="test")

  monkeypatch.setattr(telegram_objects, "bot", MockBot)
  client = TestClient(app)
  response = client.get("/")
  assert response.status_code == 200
  assert response.headers["content-type"] == "text/html; charset=utf-8"


def test_webhook_with_correct_header_set(valid_flow_with_webhook_activations: str) -> None:
  client = TestClient(app)
  add_webhooks(load(valid_flow_with_webhook_activations))
  response = client.post("/hook_with_header", headers={"x-app-token": "secret-token"})
  assert response.status_code == 200


def test_webhook_with_correct_query_parameter_set(valid_flow_with_webhook_activations: str) -> None:
  client = TestClient(app)
  add_webhooks(load(valid_flow_with_webhook_activations))
  response = client.post("/hook_with_query_params?token=secret")
  assert response.status_code == 200


def test_webhook_without_correct_header_set(valid_flow_with_webhook_activations: str) -> None:
  client = TestClient(app)
  add_webhooks(load(valid_flow_with_webhook_activations))
  response = client.post("/hook_with_header", headers={"x-app-token": "invalid-token"})
  assert response.status_code != 200


def test_webhook_without_correct_query_parameter_set(valid_flow_with_webhook_activations: str) -> None:
  client = TestClient(app)
  add_webhooks(load(valid_flow_with_webhook_activations))
  response = client.post("/hook_with_query_params?token=invalid")
  assert response.status_code != 200


def test_webhook_with_failing_precondition(valid_flow_with_webhook_activations: str) -> None:
  client = TestClient(app)
  add_webhooks(load(valid_flow_with_webhook_activations))
  response = client.post("/hook_with_failing_precondition?token=secret")
  assert response.status_code == 200
  assert response.json() == {"message": "The condition is not met. Skipping the handler."}


def test_telegram_webhook_invalid_secret_in_headers(monkeypatch: pytest.MonkeyPatch) -> None:
  with monkeypatch.context() as m:
    m.setenv("WEB_BOT_WEBHOOK_SECRET", "secret")
    client = TestClient(app)
    add_bot_webhook("/webhook")
    response = client.post("/webhook", headers={"x-telegram-bot-api-secret-token": "invalid_secret"})
    assert response.status_code == 403


def test_telegram_webhook_invalid_body() -> None:
  client = TestClient(app)
  add_bot_webhook("/webhook")
  response = client.post("/webhook", content="invalid_body")
  assert response.status_code == 400


def test_telegram_webhook_unexpected_body() -> None:
  client = TestClient(app)
  add_bot_webhook("/webhook")
  response = client.post("/webhook", json={})
  assert response.status_code == 400
