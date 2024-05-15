from __future__ import annotations

import logging
import typing as t

from shipany.bot.contrib.aiogram.action_dispatcher import GoToNextAction, GoToStep
from shipany.bot.contrib.aiogram.renders.context_proxy import proxy
from shipany.bot.jsonlogic import apply

if t.TYPE_CHECKING:
  from shipany.bot.contrib.aiogram.context import Context
  from shipany.bot.conversation.v1.models.actions import TransitionAction

logger = logging.getLogger(__name__)


async def process(ctx: Context, action: TransitionAction) -> GoToStep | GoToNextAction:
  if action.condition is None:
    return GoToStep(step_id=action.next_step)

  if apply(action.condition, proxy(ctx)):
    return GoToStep(step_id=action.next_step)

  return GoToNextAction()
