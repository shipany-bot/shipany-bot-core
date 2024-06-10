import json

import pytest


@pytest.fixture()
def valid_flow_with_webhook_activations() -> str:
  return json.dumps(
    {
      "$schema": "https://shipany.bot/schemata/0.1.0/schema.json",
      "name": "welcome-bot",
      "description": "A simple bot welcoming users.",
      "version": "1.0.0",
      "conversations": [
        {
          "$id": "start",
          "activations": [
            {"command": "/start", "next-step": "start"},
            {
              "webhook": {
                "path": "/hook_with_header",
                "method": "POST",
                "status-code-ok": "200",
                "status-code-error": "400",
                "expect": {"headers": {"x-app-token": "secret-token"}, "query-parameters": {}},
              },
              "next-step": "start",
            },
            {
              "webhook": {
                "path": "/hook_with_query_params",
                "method": "POST",
                "status-code-ok": "200",
                "status-code-error": "400",
                "expect": {"headers": {}, "query-parameters": {"token": "secret"}},
              },
              "next-step": "start",
            },
            {
              "webhook": {
                "path": "/hook_with_failing_precondition",
                "method": "POST",
                "status-code-ok": "200",
                "status-code-error": "400",
                "expect": {"headers": {}, "query-parameters": {"token": "secret"}},
              },
              "condition": {"==": [1, 2]},
              "next-step": "start",
            },
          ],
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
