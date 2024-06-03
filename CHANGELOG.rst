
2024-06-03
==========

Added
-----

- `HttpRequest@1`: action to communicate with a server using HTTP.
- `JsonPathAction@1`: action to extract data from a JSON response.
- `shipany-bot-cli` supports conversation flows supplied as URLs.
- VS Code: added debug configuration

- New interfaces `shipany.bot.runtime.secrets.SecretsProvider` and `shipany.bot.runtime.captures.CapturesProvider` to enable the injection of secrets and captures into the conversation flow. The `SecretsProvider` interface allows you to provide secrets to the conversation flow, while the `CapturesProvider` interface allows you to provide captures to the conversation flow.
- The corresponding implementations `shipany.bot.runtime.secrets.StubSecretsProvider` and `shipany.bot.runtime.captures.InMemoryCapturesProvider` to provide basic functionality.
- The `inject` package to enable runtime dependency injection. One can now inject such dependencies as `SecretsProvider` and `CapturesProvider`.
- The `BrokenAction@1` and `BrokenAction@2` actions to test edge cases.
- `shipany-bot-cli run` command now supports `--secret` option. This option allows you to pass the secret in the from of the `key=value`.Later, the value can be referenced by using the `{{ secrets.<key> }}` template.
- `secrets.` template to reference secrets in the conversation flow.

Changed
-------

- README.md: updated the documentation to reflect the new actions.
- New dependencies: added the `jsonpath-ng` and `httpx` libraries to the `pyproject.toml`.
- Action models became frozen.
- Action models allow extra fields explicitly for backward compatibility.
- Jinja2 templates do not auto escape anymore.

- Along with files, the `shipany-bot-cli run` command supports URL as input for conversation flows. The URL should be a valid URL that points to a JSON file containing the conversation flow.
- The `shipany-bot-cli run` assumes that the `aiogram` backend is used by default. If you are using a different backend, you can specify it using the `--backend` option. The only supported backend now is `aiogram`, though.

Fixed
-----

- Conversation flow may contain two or more actions in a row which communicate something to the user. Prior to this fix, a bot could not reply and then follow up with another message. This has been fixed.

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
