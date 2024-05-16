## shipany-bot-core

No-code framework for building chatbots with ease. Only Telegram is supported at the moment.

### Features
- No-code
- Jinja2 templates
- Conditional logic (jsonlogic)

Writing your first bot is as simple as writing a JSON file.

Look at the example below:

```json
{
  "$schema": "https://shipany.bot/schemata/v1.0/flow.json",
  "name": "Echo bot",
  "description": "A simple echo bot",
  "version": "1.0.0",
  "conversations": [{
    "$id": "echo",
    "activations": [{
      "event": "on-message",
      "next-step": "reply-in-return"
    }],
    "steps": [{
      "$id": "reply-in-return",
      "actions": [{
        "type": "reply",
        "content": "{{message.text}}"
      }]
    }]
  }]
}
```

Apart from descriptive fields like `name`, `description`, and `version`, the bot schema consists of `conversations` array. Each conversation has a unique `$id` and contains `activations` and `steps` arrays.

`activations` array contains objects that define when the conversation should be triggered. In this example, the conversation is triggered when the bot receives a message.

`steps` array contains objects that define what the bot should do when the conversation is triggered. In this example, the bot replies with the same message it received.

The bot schema is validated against the JSON schema, so you can be sure that your bot is correctly defined.

More examples can be found in the `examples` directory.

### Installation

Before you run the bot, you need to create a bot with Telegram BotFather and get the token.

Once you have the token, paste it into `.test.env` file and rename it to `.env`.

Then, install the package with 'cli' extra and run the bot:
```bash
pip install 'shipany-bot-core[cli]'
shipany-bot-cli run examples/echo-bot.json
```

Go to Telegram and start chatting with your bot! Have fun!
