from pydantic import BaseModel, Field

from .actions import ActionTypes


class Step(BaseModel):
  step_id: str = Field(alias="$id")
  actions: ActionTypes


Steps = list[Step]
