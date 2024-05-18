
2024-05-18
==========

Removed
-------

- `FunctionAction` was removed.

Added
-----

- Actions are now versioned and isolated from the rest of the conversation schema. This means that you can use a built-in action or create your own. The action is a class that implements the `BaseModel` interface. The action class must be under the `shipany.bot.actions.<action_name>.v<version>` module. The action class will be loaded dynamically by the bot when it is needed.

Changed
-------

- Schema change: now actions must have a `name` field. It refers to versioned class under `shipany.bot.actions` module.
- The existing actions were updated to have the `name` field. Now they are `MessageAction@1`, `StateAction@1` and `TransitionAction@1`.
- Structure of imports has changed to enable simple core extensions.
