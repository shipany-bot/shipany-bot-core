import typing as t
from enum import StrEnum

from pydantic import BaseModel, Field


class SupportedMessageActionTypes(StrEnum):
  answer = "answer"
  reply = "reply"


class MessageAction(BaseModel):
  name: t.Literal["MessageAction@1"]
  action_type: SupportedMessageActionTypes = Field(alias="type")
  content: str
