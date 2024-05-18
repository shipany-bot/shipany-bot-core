from __future__ import annotations

import logging
import typing as t

from shipany.bot.conversation import errors

if t.TYPE_CHECKING:
  from shipany.bot.conversation.models import BaseAction, Step, Steps

logger = logging.getLogger(__name__)


class EventHandler:
  steps: Steps

  def __init__(self: t.Self, steps: Steps, *, begin_with_step_id: str) -> None:
    self.steps = steps
    self.begin_with_step_id = begin_with_step_id

  def _get_step(self: t.Self, step_id: str) -> Step:
    for step in self.steps:
      if step.step_id == step_id:
        return step
    raise errors.NoStepFoundError(step_id)

  def _get_actions(self: t.Self, step_id: str) -> list[BaseAction]:
    step = self._get_step(step_id)
    return step.actions

  def traverse_actions(self: t.Self) -> t.Generator[BaseAction | None, str, None]:
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
