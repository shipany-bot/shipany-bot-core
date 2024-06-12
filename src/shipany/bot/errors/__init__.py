class ShipAnyError(Exception):
  pass


class FlowValidationError(ShipAnyError):
  pass


class NotImplementedError(ShipAnyError):
  pass
