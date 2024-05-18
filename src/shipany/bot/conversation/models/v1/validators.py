from __future__ import annotations

import typing as t

from shipany.bot.errors import FlowValidationError

from .activations import CommandActivation

if t.TYPE_CHECKING:
  from .flow import Flow


def check_for_orphaned_conversations(flow: Flow) -> None:
  """
  Check for orphaned conversations in the flow
  """
  for conversation in flow.conversations:
    if not conversation.activations:
      raise FlowValidationError(f"Conversation {conversation.conversation_id} has no activations")


def check_missed_start_state(flow: Flow) -> None:
  """
  Check for missed start state in the flow
  """

  for conversation in flow.conversations:
    steps = {step.step_id for step in conversation.steps}
    for activation in conversation.activations:
      if isinstance(activation, CommandActivation) and activation.next_step not in steps:
        raise FlowValidationError(f"Conversation {conversation.conversation_id} has no start state")


all_checks: set[t.Callable[[Flow], None]] = {
  check_for_orphaned_conversations,
  check_missed_start_state,
}
