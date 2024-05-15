from __future__ import annotations

import logging
import typing as t
from typing_extensions import Self

from shipany.bot.conversation.v1 import errors

if t.TYPE_CHECKING:
  from shipany.bot.conversation.v1.models import ActionTypes, Step, Steps
  from shipany.bot.conversation.v1.models.actions import ActionType

logger = logging.getLogger(__name__)


class EventHandler:
  steps: Steps

  def __init__(self: Self, steps: Steps, *, begin_with_step_id: str) -> None:
    self.steps = steps
    self.begin_with_step_id = begin_with_step_id

  def _get_step(self: Self, step_id: str) -> Step:
    for step in self.steps:
      if step.step_id == step_id:
        return step
    raise errors.NoStepFoundError(step_id)

  def _get_actions(self: Self, step_id: str) -> ActionTypes:
    step = self._get_step(step_id)
    return step.actions

  def traverse_actions(self: Self) -> t.Generator[ActionType | None, str, None]:
    actions = iter(self._get_actions(self.begin_with_step_id).copy())
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
        new_actions = self._get_actions(next_step_id).copy()
        actions = iter(new_actions)
        yield None  # Important! Send None to avoid skipping the next action from new_actions
      else:
        logger.info("No transition to step")
