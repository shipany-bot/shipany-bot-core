from __future__ import annotations

import typing as t
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from shipany.bot.persistency.scopes import Scope  # noqa: TCH001


class SupportedStateActionTypes(StrEnum):
  remove = "remove"
  store = "store"
  load = "load"


class StateAction(BaseModel):
  """Action to store or retrieve a state with respect to the scope.

  Examples:
  - Set new variable in chat scope:
    ```json
    {
      "name": "StateAction@1",
      "type": "store",
      "key": "admin",
      "value": "John Doe",
      "scope": ["chat"],
    }
    ```
  - Remove variable from chat scope:
    ```json
    {
      "name": "StateAction@1",
      "type": "remove",
      "key": "admin",
      "scope": ["chat"],
    }
    ```
  - Set new variable in user state:
    ```json
    {
      "name": "StateAction@1",
      "type": "store",
      "key": "",
      "value": "Echo bot",
      "scope": ["user"]
    }
    ```
  - Set new variable in user state with expiration time:
    ```json
    {
      "name": "StateAction@1",
      "type": "store",
      "key": "mute",
      "value": "1",
      "ttl": 3600,
      "scope": ["user"]
    }
    ```

  - Load variable from chat scope to current session:
    ```json
    {
      "name": "StateAction@1",
      "type": "load",
      "key": "admin",
      "scope": ["chat"]
    }
    ```

  """

  name: t.Literal["StateAction@1"]
  """Action name."""

  action_type: SupportedStateActionTypes = Field(alias="type")
  """Action type."""

  key: str
  """Name of state to store or retrieve."""

  value: str | None = None
  """Value to store. It can't be None if action_type is store. It may contain Jinja2 template using {{ notation }}."""

  scope: list[Scope] = []
  """Scope of state action. Default is empty list which means global scope available for all."""

  ttl: int | None = None
  """Time to live in seconds. Default is None which means no expiration."""

  model_config = ConfigDict(extra="allow", frozen=True)

  @model_validator(mode="after")
  def validate_value(self: t.Self) -> t.Self:
    if self.action_type == SupportedStateActionTypes.store and self.value is None:
      raise ValueError("Value cannot be None for 'store' action type.")
    return self
