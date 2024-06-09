from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from .base import BaseActivation


class WebhookMethod(StrEnum):
  """Webhook HTTP methods."""

  POST = "POST"


class Expectation(BaseModel):
  """Expectation model. Contains information about the expected HTTP attributes of the request.
  Helps to safeguard the webhook from malicious requests."""

  headers: dict[str, str] = Field(description="Expected headers.")
  query_params: dict[str, str] = Field(alias="query-parameters", description="Expected query parameters.")
  model_config = ConfigDict(extra="allow", frozen=True)


class WebhookParameters(BaseModel):
  """Webhook parameters."""

  path: str = Field(description="Webhook endpoint.")
  status_code_ok: int = Field(alias="status-code-ok", description="Expected status code for a successful response.")
  status_code_error: int = Field(alias="status-code-error", description="Expected status code for an error response.")
  method: WebhookMethod = Field(description="HTTP method to use for the webhook.")
  expect: Expectation = Field(description="Expected parameters of the incoming request. Use for bot-side validation.")
  model_config = ConfigDict(extra="allow", frozen=True)


class WebhookActivation(BaseActivation):
  """Webhook model. Contains information about the webhook path and the list of actions to perform in response"""

  webhook: WebhookParameters = Field(description="Webhook parameters.")
  model_config = ConfigDict(extra="allow", frozen=True)
