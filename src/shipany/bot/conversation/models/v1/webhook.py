from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from .action import BaseAction  # noqa: TCH001


class WebhookMethod(StrEnum):
  """Webhook HTTP methods."""

  POST = "POST"


class Expectation(BaseModel):
  """Expectation model. Contains information about the expected HTTP attributes of the request.
  Helps to safeguard the webhook from malicious requests."""

  headers: dict[str, str] = Field(description="Expected headers.", default_factory=dict)
  query_params: dict[str, str] = Field(
    alias="query-parameters", description="Expected query parameters.", default_factory=dict
  )
  model_config = ConfigDict(extra="forbid", frozen=True)


class Webhook(BaseModel):
  """Webhook model. Contains information about the webhook path and the list of actions to perform in response"""

  webhook_id: str = Field(alias="$id", description="Unique identifier of the webhook.")
  path: str = Field(description="Webhook endpoint.")
  status_code_ok: int = Field(200, description="Expected status code for a successful response.")
  status_code_error: int = Field(400, description="Expected status code for an error response.")
  method: WebhookMethod = Field(description="HTTP method to use for the webhook.")
  expect: Expectation = Field(
    description="Expected parameters of the incoming request. Use for server-side validation."
  )
  actions: list[BaseAction] = Field([], description="List of actions to perform in the step")
  model_config = ConfigDict(extra="allow", frozen=True)
