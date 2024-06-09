from __future__ import annotations

from pydantic import BaseModel, Field

from .action import BaseAction  # noqa: TCH001


class Step(BaseModel):
  """Represents a single step in the conversation flow. Contains a list of actions to perform.

  Usually, a step is a single message sent by the bot or a user's response. But it can also be a complex action like
  sending a file or making an API request. The actions have a specific order and are executed one by one unless
  transition to another step is triggered. The step can have a unique identifier to be referenced from other steps.
  Actions may refer to steps within the same conversation.
  """

  step_id: str = Field(alias="$id")
  actions: list[BaseAction] = Field([], description="List of actions to perform in the step")


Steps = list[Step]
