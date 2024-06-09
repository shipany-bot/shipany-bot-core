from pydantic import BaseModel, ConfigDict, Field


class BaseAction(BaseModel):
  """Base action model.

  Requires a name field to be present to identify the action class.

  It is allowed to have any additional fields in the action configuration. The fields are validated
  against the action schema defined in the action registry."""

  """Name of the action. The action must be registered in the action registry under this name."""
  name: str = Field(
    pattern=r"([a-zA-Z]+)@(\d+)",
    description="Action name in the format of `name@version`. Name must be alphanumeric. Version must be a number.",
  )

  model_config = ConfigDict(extra="allow")
