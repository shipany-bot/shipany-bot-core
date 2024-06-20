import typing as t

from pydantic import BaseModel


class BrokenAction(BaseModel):
  name: t.Literal["BrokenAction@4"]
