from __future__ import annotations

import logging
import typing as t

from shipany.bot.contrib.aiogram.renders.context_proxy import proxy
from shipany.bot.conversation.handlers.actions import Continue, GoToStep
from shipany.bot.jsonlogic import apply

if t.TYPE_CHECKING:
  from shipany.bot.actions.transition_action.v1 import TransitionAction
  from shipany.bot.contrib.aiogram.context import Context

logger = logging.getLogger(__name__)


def process(ctx: Context, action: TransitionAction) -> GoToStep | Continue:
  if action.condition is None:
    return GoToStep(step_id=action.next_step)

  if apply(action.condition, proxy(ctx)):
    return GoToStep(step_id=action.next_step)

  return Continue()
