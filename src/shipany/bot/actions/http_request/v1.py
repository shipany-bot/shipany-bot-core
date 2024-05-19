from __future__ import annotations

import typing as t
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, JsonValue


class HttpMethods(StrEnum):
  GET = "GET"
  POST = "POST"
  PUT = "PUT"
  PATCH = "PATCH"
  DELETE = "DELETE"


class HttpRequest(BaseModel):
  name: t.Literal["HttpRequest@1"]
  method: HttpMethods = Field(..., title="HTTP method")
  url: HttpUrl = Field(..., description="URL to send the request to")
  headers: dict[str, str] | None = Field(None, description="Headers to send with the request")
  query_string_parameters: dict[str, str] | None = Field(
    None, description="Query string parameters to send with the request"
  )
  basic_auth: str | None = Field(
    None, description="Basic auth credentials to use with the request. Should be in the format 'username:password'"
  )
  timeout: float | None = Field(None, description="Timeout for the request in seconds", le=300.0)
  body: JsonValue | None = Field(None, description="Body to send with the request (if applicable)")
  captures: dict[str, str] | None = Field(
    None,
    description="Capture values from the response. The key is the name of the capture, and the value "
    "is a Jinja template to extract the value from the response. For example, `{'foo': 'response.status_code'}` "
    "would extract the value of `response.status_ocde` and store it as 'foo' variable. Available variables are "
    "`response.content`, `response.status_code`, `response.text`, and `response.headers`. The `response.content` "
    "is decoded as a string. Consider post-processing the value with Jinja filters if necessary. If JSON response "
    "is expected, apply `JsonPath@1` action after.",
  )

  model_config = ConfigDict(extra="allow", frozen=True)
