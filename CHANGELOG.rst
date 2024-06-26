
.. _changelog-0.7.0a1:

0.7.0a1 — 2024-06-28
====================

Added
-----

- Webhook mode is supported now. You need to configure such env variables like `TELEGRAM_WEBHOOK_URL` and `WEB_BOT_WEBHOOK_PATH` to enable this mode. The Telegram will send messages to the specified URL using the optional secret `WEB_BOT_WEBHOOK_SECRET`. You need to ensure that the bot properly configured behind the proxy if there is any. You can use any external webhook payload delivery service to test the connection locally.
- In order to track the events when the web server is ready, the new class `WebserverEventsDispatcher` was introduced. It allows you to subscribe to the `on_startup`, `on_shutdown`, and `on_updates` events.

.. _changelog-0.6.0a1:

0.6.0a1 — 2024-06-20
====================

Removed
-------

- `conversation.model.v1` module removed. All the classes moved to `conversation.model` module. In case of any schema changes, the versioning will be handled by the package itself.

Added
-----

- Along with the bot itself, one can run webserver to serve webhooks - http calls to endpoints defined as conversation activations.
- `fastapi` is used as the webserver framework.
- `shipany-bot-cli run` command now accepts `--no-web` option to disable the webserver.
- `WebhookActivation` class added to support webhook activations.

- A new entity called `Scope` that defines a scope for a state. The state can be stored or retrieved either in/from the user, chat or both scopes. If no scope is defined, the state is temporary and is not stored in the persistency.
- A debugging configuration for the VS Code editor.
- The abstract class `HandlesGenerator`, which can be extended to provide a custom implementation for particular persistency storage.
- The inherited class `AiogramHandleGenerator` provides a default implementation for the persistency storage using the context of the `aiogram` events and the given scope.

Changed
-------

- Coverage report includes all the files now (even tests).
- `Context` class moved to `shipany.bot.runtime` module.
- `ExtendedContext` class derives from `Context` class now and carries the Telegram event data.
- `AiogramEventHandler` class renamed to `ActivationHandler` class.
- `ActivationHandler` class is telegram backend agnostic now.

- To load a state to the current scope from persistency, use the `StateAction@1` class with the `load` type. The loaded value will be available to any following action within given step or steps.
- The `StateAction@1` class has a new type called `remove`. It removes the state from the selected scope. Prior to that, one could use the `StateAction@1` class with the `store` type and the `null` value to remove the state. Now, it is prohibited.
- Leverage the `inject` library to inject runtime bindings.
- Methods can be defined in `bindings` modules cascadingly. The `bindings` module can be nested in another `bindings` module.
- `ExtendedContext` is renamed to `ConversationContext` and moved away from the `aiogram` package.
- JsonLogic uses the `ConversationContext` as data provider directly.
- The `VarOperation` class comes with the scope parameter. It is used to define the scope of the variable. The scope can be `user` or `chat`. If no scope is defined, the variable is retrieved from the session.

Fixed
-----

- Conversation flow may contain two or more actions in a row which communicate something to the user. Prior to this fix, a bot could not reply and then follow up with another message. This has been fixed.

Security
--------

- The actions can refer only to a state in the current temporary scope. Before, actions could use a shared state and compromise the security.
- The jinja2 templates will not be able to expose secrets anymore when `safe=False` is set.

.. _changelog-0.5.0a1:

0.5.0a1 — 2024-06-03
====================

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

.. _changelog-0.4.0a1:

0.4.0a1 — 2024-05-18
====================

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
