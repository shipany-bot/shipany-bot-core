import typing as t


class ShipAnyError(Exception):
  pass


class FlowValidationError(ShipAnyError):
  pass


class NotImplementedError(ShipAnyError):
  pass


class ActionNotImplementedError(ShipAnyError):
  def __init__(self: t.Self, action_name: str, details: str) -> None:
    super().__init__(f"Action '{action_name}' is not implemented: {details}")
