from __future__ import annotations

import json
import typing as t

import inject
import pytest

from shipany.bot.contrib.aiogram import bindings as aiogram_bindings
from shipany.bot.providers.captures import CapturesProvider, InMemoryCapturesProvider
from shipany.bot.providers.secrets import SecretsProvider, StubSecretsProvider

BinderCallable = t.Callable[[inject.Binder], None]


@pytest.fixture()
def setup_captures() -> t.Mapping[str, str]:
  return {}


@pytest.fixture()
def captures_provider(setup_captures: t.Mapping[str, str]) -> BinderCallable:
  def _runtime_bindings(binder: inject.Binder) -> None:
    captures_provider = InMemoryCapturesProvider(initial_value=setup_captures)
    binder.bind(CapturesProvider, captures_provider)

  return _runtime_bindings


@pytest.fixture()
def secrets_provider() -> BinderCallable:
  def _secrets_provider(binder: inject.Binder) -> None:
    binder.bind(SecretsProvider, StubSecretsProvider())

  return _secrets_provider


@pytest.fixture()
def aiogram_default_bindings() -> BinderCallable:
  def _aiogram_default_bindings(binder: inject.Binder) -> None:
    aiogram_bindings.default_bindings(binder)

  return _aiogram_default_bindings


@pytest.fixture()
def all_bindings(
  captures_provider: BinderCallable,
  secrets_provider: BinderCallable,
  aiogram_default_bindings: BinderCallable,
) -> BinderCallable:
  def _all_bindings(binder: inject.Binder) -> None:
    captures_provider(binder)
    secrets_provider(binder)
    aiogram_default_bindings(binder)

  return _all_bindings


@pytest.fixture(autouse=True)
def _runtime_injections(all_bindings: BinderCallable) -> None:
  inject.configure(all_bindings, clear=True, allow_override=True)


@pytest.fixture()
def valid_flow_with_conditional_responses() -> str:
  return json.dumps(
    {
      "$schema": "https://shipany.bot/schemata/0.1.0/schema.json",
      "name": "welcome-bot",
      "description": "A simple bot welcoming users.",
      "version": "1.0.0",
      "conversations": [
        {
          "$id": "start",
          "activations": [{"event": "on-message", "next-step": "start"}],
          "steps": [
            {
              "$id": "start",
              "actions": [
                {
                  "name": "TransitionAction@1",
                  "condition": {"in": ["hi", {"var": "message.text"}]},
                  "next-step": "hello-step",
                },
                {
                  "name": "MessageAction@1",
                  "type": "reply",
                  "content": "👋!",
                },
              ],
            },
            {
              "$id": "hello-step",
              "actions": [
                {
                  "name": "MessageAction@1",
                  "type": "reply",
                  "content": "Hey there 👋!",
                }
              ],
            },
          ],
        }
      ],
    }
  )


@pytest.fixture()
def valid_flow_with_unknown_action() -> str:
  return json.dumps(
    {
      "$schema": "https://shipany.bot/schemata/0.1.0/schema.json",
      "name": "welcome-bot",
      "description": "A simple bot welcoming users.",
      "version": "1.0.0",
      "conversations": [
        {
          "$id": "start",
          "activations": [{"event": "on-message", "next-step": "start"}],
          "steps": [
            {
              "$id": "start",
              "actions": [
                {
                  "name": "NotImplementedAction@1",
                },
              ],
            },
          ],
        }
      ],
    }
  )


@pytest.fixture()
def valid_flow_with_broken_v1_action() -> str:
  return json.dumps(
    {
      "$schema": "https://shipany.bot/schemata/0.1.0/schema.json",
      "name": "welcome-bot",
      "description": "A simple bot welcoming users.",
      "version": "1.0.0",
      "conversations": [
        {
          "$id": "start",
          "activations": [{"event": "on-message", "next-step": "start"}],
          "steps": [
            {
              "$id": "start",
              "actions": [
                {
                  "name": "BrokenAction@1",
                },
              ],
            },
          ],
        }
      ],
    }
  )


@pytest.fixture()
def valid_flow_with_broken_v2_action() -> str:
  return json.dumps(
    {
      "$schema": "https://shipany.bot/schemata/0.1.0/schema.json",
      "name": "welcome-bot",
      "description": "A simple bot welcoming users.",
      "version": "1.0.0",
      "conversations": [
        {
          "$id": "start",
          "activations": [{"event": "on-message", "next-step": "start"}],
          "steps": [
            {
              "$id": "start",
              "actions": [
                {
                  "name": "BrokenAction@2",
                },
              ],
            },
          ],
        }
      ],
    }
  )


@pytest.fixture()
def valid_flow_with_store_action() -> str:
  return json.dumps(
    {
      "$schema": "https://shipany.bot/schemata/0.1.0/schema.json",
      "name": "welcome-bot",
      "description": "A simple bot welcoming users.",
      "version": "1.0.0",
      "conversations": [
        {
          "$id": "start",
          "activations": [{"event": "on-message", "next-step": "start"}],
          "steps": [
            {
              "$id": "start",
              "actions": [
                {
                  "name": "StateAction@1",
                  "type": "store",
                  "key": "token",
                  "value": "value",
                },
              ],
            },
          ],
        }
      ],
    }
  )
