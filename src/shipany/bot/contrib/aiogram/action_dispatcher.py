from __future__ import annotations

import inspect
import logging
import re
import typing as t

from aiogram.methods import TelegramMethod  # noqa: TCH002
from pydantic import BaseModel, ValidationError, validate_call

from shipany.bot.conversation.models.v1.action import BaseAction  # noqa: TCH001

from .context import Context  # noqa: TCH001

logger = logging.getLogger(__name__)


class Terminate(BaseModel):
  pass


class AwaitMethodAndContinue(BaseModel):
  value: TelegramMethod


class Continue(BaseModel):
  pass


class GoToStep(BaseModel):
  step_id: str


DispatchedResult = Terminate | Continue | GoToStep | AwaitMethodAndContinue


def _split_action_name(action_name: str) -> tuple[str, str]:
  # It is safe to just split by '@' because action name is validated as BaseAction.name field
  matches = action_name.split("@")
  return matches[0], "v" + matches[1]


def _camel_to_snake(name: str) -> str:
  """Transforms CamelCase to snake_case."""
  name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
  return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def _find_action_module(module_name: str, class_name: str, class_version: str) -> type[BaseModel]:
  full_module_name = f"shipany.bot.actions.{module_name}.{class_version}"
  try:
    module = __import__(full_module_name, fromlist=[class_version])
  except ImportError:
    raise NotImplementedError(f"Module {full_module_name} is not importable") from None

  try:
    action_model_class = getattr(module, class_name)
  except AttributeError:
    raise NotImplementedError(f"Class {class_name} cannot be found in {full_module_name}") from None

  if not issubclass(action_model_class, BaseModel):
    raise TypeError(f"Action {action_model_class} is not a Pydantic model")

  return action_model_class


@t.runtime_checkable
class ModuleWithProcessFunction(t.Protocol):
  def process(self: t.Self, ctx: Context, action: BaseModel) -> DispatchedResult: ...


def _func_process_module(module_name: str, class_name: str, class_version: str) -> ModuleWithProcessFunction:
  full_module_name = f"shipany.bot.contrib.aiogram.process.{module_name}.{class_version}"
  try:
    module = __import__(full_module_name, fromlist=[class_version])
  except ImportError:
    raise NotImplementedError(f"Module {full_module_name} is not importable") from None

  try:
    if not isinstance(module, ModuleWithProcessFunction):
      raise NotImplementedError(f"process() method in {full_module_name} should have 2 parameters: ctx, action")
  except AttributeError:
    raise NotImplementedError(f"process() method cannot be found in {full_module_name}") from None

  return module


@validate_call
async def handle(action: BaseAction, ctx: Context) -> DispatchedResult:
  class_name, class_version = _split_action_name(action.name)
  module_name = _camel_to_snake(class_name)

  action_model_class = _find_action_module(module_name, class_name, class_version)

  try:
    transformed_action = action_model_class.model_validate(action.model_dump())
  except ValidationError:
    logger.error(f"Cannot cast {action.name} to {module_name}.{class_name} class", exc_info=True)
    raise

  process_module = _func_process_module(module_name, class_name, class_version)

  if not inspect.iscoroutinefunction(process_module.process):
    return process_module.process(ctx, transformed_action)

  return await process_module.process(ctx, transformed_action)
