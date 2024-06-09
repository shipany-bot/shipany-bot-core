import typing as t


class ConversationRuntimeError(RuntimeError):
  pass


class NoEventFoundError(ConversationRuntimeError):
  def __init__(self: t.Self, event_name: str, step_id: str) -> None:
    super().__init__(f"Could not find event '{event_name}' in step '{step_id}'")


class NoStepFoundError(ConversationRuntimeError):
  def __init__(self: t.Self, step_id: str) -> None:
    super().__init__(f"Could not find step with id '{step_id}'")


class ActionNotImplementedError(ConversationRuntimeError):
  def __init__(self: t.Self, action_name: str, details: str) -> None:
    super().__init__(f"Action '{action_name}' is not implemented: {details}")
