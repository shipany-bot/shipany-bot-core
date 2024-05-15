from typing_extensions import Self


class ConversationRuntimeError(RuntimeError):
  pass


class NoEventFoundError(ConversationRuntimeError):
  def __init__(self: Self, event_name: str, step_id: str) -> None:
    super().__init__(f"Could not find event '{event_name}' in step '{step_id}'")


class NoStepFoundError(ConversationRuntimeError):
  def __init__(self: Self, step_id: str) -> None:
    super().__init__(f"Could not find step with id '{step_id}'")
