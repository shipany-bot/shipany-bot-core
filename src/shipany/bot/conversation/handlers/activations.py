from __future__ import annotations

import logging
import typing as t

from shipany.bot.contrib.aiogram.renders.context_proxy import proxy
from shipany.bot.conversation import errors
from shipany.bot.conversation.handlers.actions import (
  AwaitObjectAndContinue,
  Continue,
  DispatchedResult,
  GoToStep,
  Terminate,
  handle,
)
from shipany.bot.jsonlogic import JsonLogic, apply

if t.TYPE_CHECKING:
  from shipany.bot.conversation.models.action import BaseAction
  from shipany.bot.conversation.models.activations import Activation
  from shipany.bot.conversation.models.steps import Step, Steps
  from shipany.bot.runtime.context import Context

logger = logging.getLogger(__name__)


class ActivationHandler:
  def __init__(self: t.Self, context: Context, activation: Activation) -> None:
    self.begin_with_step_id = activation.next_step
    self.context = context
    if activation.condition:
      self.check_preconditions(activation.condition)

  def _get_step(self: t.Self, steps: Steps, step_id: str) -> Step:
    for step in steps:
      if step.step_id == step_id:
        return step
    raise errors.NoStepFoundError(step_id)

  def _get_actions(self: t.Self, steps: Steps, step_id: str) -> list[BaseAction]:
    step = self._get_step(steps, step_id)
    return step.actions

  def check_preconditions(self: t.Self, condition: JsonLogic) -> None:
    logger.info("Checking condition %s", condition)
    if not apply(condition, proxy(self.context)):
      logger.info("The condition is not met. Skipping the handler.")
      raise errors.ActivationPreconditionNotMeetError

  def traverse_actions(self: t.Self, steps: Steps) -> t.Generator[BaseAction | None, str, None]:
    actions = iter(self._get_actions(steps, self.begin_with_step_id).copy())
    while True:
      try:
        logger.info("Getting next action")
        action = next(actions)
      except StopIteration:
        logger.info("No more actions to execute")
        break

      logger.info("Sending action: %s", action)
      next_step_id = yield action
      if next_step_id:
        logger.info("Received transition to step: %s", next_step_id)
        new_actions = self._get_actions(steps, next_step_id).copy()
        actions = iter(new_actions)
        yield None  # Important! Send None to avoid skipping the next action from new_actions
      else:
        logger.info("No transition to step")

  async def __call__(self: t.Self, steps: Steps) -> None:
    logger.info("Event handler called")
    actions = self.traverse_actions(steps)
    for action in actions:
      logger.info("Executing action: %s", action)
      if not action:  # pragma: no cover
        continue  # unreachable code but makes mypy happy
      try:
        result: DispatchedResult = await handle(action, self.context)
      except (NotImplementedError, TypeError) as e:
        raise errors.ActionNotImplementedError(action.name, str(e)) from None

      match result:
        case Terminate():
          return
        case AwaitObjectAndContinue(value=value):
          await value
          continue
        case Continue():
          continue
        case GoToStep(step_id=step_id):
          logger.info("Transitioning to next step: %s", step_id)
          actions.send(step_id)
        case _:  # pragma: no cover
          t.assert_never(result)
