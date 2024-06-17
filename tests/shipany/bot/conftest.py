from __future__ import annotations

import json
import typing as t

import inject
import pytest

from shipany.bot.contrib.aiogram import bindings as aiogram_bindings
from shipany.bot.conversation.loader import load
from shipany.bot.persistency.handles import HandleGeneratorFactory
from shipany.bot.providers.captures import CapturesProvider, InMemoryCapturesProvider
from shipany.bot.providers.secrets import SecretsProvider, StubSecretsProvider

if t.TYPE_CHECKING:
  from pathlib import Path

  from shipany.bot.conversation.models.flow import Flow

BinderCallable = t.Callable[[inject.Binder], None]


@pytest.fixture()
def setup_captures() -> t.Mapping[str, str]:
  return {}


@pytest.fixture()
def setup_locals() -> t.Mapping[str, str]:
  return {}


@pytest.fixture()
def setup_secrets() -> t.Mapping[str, str]:
  return {}


@pytest.fixture()
def captures_provider(setup_captures: t.Mapping[str, str], setup_locals: t.Mapping[str, str]) -> BinderCallable:
  def _runtime_bindings(binder: inject.Binder) -> None:
    captures_provider = InMemoryCapturesProvider(setup_captures=setup_captures, setup_locals=setup_locals)
    binder.bind(CapturesProvider, captures_provider)

  return _runtime_bindings


@pytest.fixture()
def secrets_provider(setup_secrets: t.Mapping[str, str]) -> BinderCallable:
  def _secrets_provider(binder: inject.Binder) -> None:
    binder.bind(SecretsProvider, StubSecretsProvider(initial_value=setup_secrets))

  return _secrets_provider


@pytest.fixture()
def captures_key_generator() -> BinderCallable:
  def _captures_key_generator(binder: inject.Binder) -> None:
    binder.bind(HandleGeneratorFactory, HandleGeneratorFactory())

  return _captures_key_generator


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
  captures_key_generator: BinderCallable,
) -> BinderCallable:
  def _all_bindings(binder: inject.Binder) -> None:
    aiogram_default_bindings(binder)
    captures_provider(binder)
    secrets_provider(binder)
    captures_key_generator(binder)

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
                  "name": "StateAction@1",
                  "type": "store",
                  "key": "username",
                  "scope": ["user"],
                  "value": "{{user.username}}",
                },
                {
                  "name": "TransitionAction@1",
                  "condition": {"in": ["hi", {"var": "message.text"}]},
                  "next-step": "hello-step",
                },
              ],
            },
            {
              "$id": "hello-step",
              "actions": [
                {
                  "name": "StateAction@1",
                  "type": "load",
                  "key": "username",
                  "scope": ["user"],
                },
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


@pytest.fixture()
def flow_from_fixture(request: pytest.FixtureRequest, flow_as_fixture: str) -> Flow:
  flow_as_str: str = request.getfixturevalue(flow_as_fixture)
  return load(flow_as_str)


@pytest.fixture()
def v1_flow_fixtures_location(flows_path_factory: t.Callable[[int], Path]) -> Path:
  return flows_path_factory(1)
