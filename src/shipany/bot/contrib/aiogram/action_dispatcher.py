from __future__ import annotations

from typing_extensions import assert_never

from aiogram.methods import TelegramMethod  # noqa: TCH002
from pydantic import BaseModel, validate_call

from shipany.bot.conversation.v1.models import actions

from .context import Context  # noqa: TCH001


class ReturnValue(BaseModel):
  value: TelegramMethod | None


class GoToNextAction(BaseModel):
  pass


class GoToStep(BaseModel):
  step_id: str


DispatchedResult = ReturnValue | GoToNextAction | GoToStep


@validate_call
async def handle(action: actions.ActionType, ctx: Context) -> DispatchedResult:
  match action:
    case actions.MessageAction():
      from shipany.bot.contrib.aiogram.actions.message import process as process_message

      return await process_message(ctx, action)
    case actions.TransitionAction():
      from shipany.bot.contrib.aiogram.actions.transition import process as process_transition

      return await process_transition(ctx, action)
    case actions.FunctionAction():
      from shipany.bot.contrib.aiogram.actions.function import process as process_function

      return await process_function(ctx, action)
    case actions.StateAction():
      from shipany.bot.contrib.aiogram.actions.state import process as process_state

      return await process_state(ctx, action)
    case _:  # pragma: no cover
      assert_never(action)  # unreachable
