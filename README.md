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
  "$schema": "https://shipany.bot/schemata/0.1.0/schema.json",
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
        "name": "MessageAction@1",
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

## Schema
The provided JSON schema describes a comprehensive model for defining conversation flows within a chatbot application. It includes definitions for various logical operations, conversation activations, steps, and actions. Here's a detailed breakdown:

### Root Schema
The root schema object defines the overall structure of the conversation model and includes the following key properties:

**$schema**: The URL of the schema definition.
**name**: The name of the bot.
**description**: A brief description of the bot's purpose.
**version**: The version of the conversation description, supporting semantic versioning.
**conversations**: An array of conversation objects, each defining a distinct conversation flow.

### Conversation Definition
Each conversation is described by:

**$id**: A unique identifier for the conversation.
**activations**: A list of conditions that trigger the conversation steps.
**steps**: A list of steps in the conversation, each representing an action or sequence of actions.

### Activation Definitions
Activations trigger specific steps within the conversation flow. There are two main types:

**CommandActivation**: Triggered by specific commands, such as "/start" or "!help".
**EventActivation**: Triggered by various events, such as message reception or user actions.

### Step Definition
Each step in a conversation includes:

**$id**: A unique identifier for the step.
**actions**: An array of actions to be performed in the step, such as sending messages or transitioning to another step.

### Action Definitions
Actions define what happens at each step. The schema includes several action types:

**MessageAction@1**: Sends a message.
**TransitionAction@1**: Transitions to another step.
**StateAction@1**: Modifies the state.
**HttpRequest@1**: Sends an HTTP request and captures the response.
**JsonPathAction@1**: Extracts data from a JSON response.

### Operation Definitions
Logical operations allow for complex conditions within the activations and actions. The schema supports:

**EqualsOperation**: Checks for equality.
**InOperation**: Checks if a value is within a list.
**AndOperation**: Logical AND operation.
**OrOperation**: Logical OR operation.
**NotOperation**: Logical NOT operation.
**VarOperation**: References a variable.
