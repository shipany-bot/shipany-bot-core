from __future__ import annotations

import typing as t

from pydantic import BaseModel, ConfigDict, Field


class JsonPathAction(BaseModel):
  name: t.Literal["JsonPathAction@1"]
  expression: str = Field(description="JsonPath expression", examples=["$.store.book[*].author"])
  captures: dict[str, str] = Field(
    default_factory=dict,
    description="Where to store the matching result. The key is the name of the capture, "
    "the value is ignored, so leave it empty. If the expression does not match anything, "
    "the capture will not be created. If the expression matches multiple values, "
    "only the first one will be captured unless you define a capture for each match.",
    examples=[{"result": ""}, {"match1": "", "match2": ""}],
  )
  input_: str = Field(
    description="The input to apply the expression to. It can be a JSON string or a Jinja2 template.",
    alias="input",
    examples=["{{response_body}}", r"{\"store\": {\"book\": [{\"author\": \"Nigel Rees\"}]}}"],
  )
  model_config = ConfigDict(extra="allow", frozen=True)
