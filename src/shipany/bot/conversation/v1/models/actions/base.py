from pydantic import BaseModel, Field


class BaseAction(BaseModel):
  action_type: str = Field(alias="type")
