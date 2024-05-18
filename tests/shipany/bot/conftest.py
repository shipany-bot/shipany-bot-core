import json

import pytest


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
