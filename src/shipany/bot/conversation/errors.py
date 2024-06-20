import typing as t


class ConversationRuntimeError(RuntimeError):
  pass


class NoStepFoundError(ConversationRuntimeError):
  def __init__(self: t.Self, step_id: str) -> None:
    super().__init__(f"Could not find step with id '{step_id}'")


class ActionNotImplementedError(ConversationRuntimeError):
  def __init__(self: t.Self, action_name: str, details: str) -> None:
    super().__init__(f"Action '{action_name}' is not implemented: {details}")


class ActivationPreconditionNotMeetError(ConversationRuntimeError):
  def __init__(self: t.Self) -> None:
    super().__init__("Activation precondition did not meet expectations")
