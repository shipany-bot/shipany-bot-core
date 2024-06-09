from __future__ import annotations

import logging
import typing as t
from functools import partial

from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.dispatcher.event.telegram import TelegramEventObserver
from aiogram.dispatcher.router import Router
from aiogram.filters.command import Command

from shipany.bot.contrib.aiogram import context
from shipany.bot.contrib.aiogram.renders.context_proxy import proxy
from shipany.bot.conversation.handlers.activations import ActivationHandler
from shipany.bot.conversation.models import (
  CommandActivation,
  Conversation,
  EventActivation,
  Flow,
)
from shipany.bot.jsonlogic import apply

if t.TYPE_CHECKING:
  from aiogram.types import TelegramObject

  from shipany.bot.conversation.models import Activation, Steps

logger = logging.getLogger(__name__)


async def handler(activation: Activation, steps: Steps, event: TelegramObject) -> None:
  with context.context(event) as ctx:
    if activation.condition is not None:
      logger.info("Checking condition %s", activation.condition)
      if not apply(activation.condition, proxy(ctx)):
        logger.info("The condition is not met. Skipping the handler.")
        raise SkipHandler

    wrapper = ActivationHandler(steps, begin_with_step_id=activation.next_step)
    await wrapper(ctx)


def activate_entry_points(conversation: Conversation, router: Router) -> None:
  for activation in conversation.activations:
    match activation:
      case CommandActivation(command=command):
        logger.info(f"Registering command handler for command '{command}'")
        router.message.register(partial(handler, activation, conversation.steps), Command(command))
      case EventActivation(event=event):
        attribute_name = event[len("on-") :].replace("-", "_")
        event_observer = getattr(router, attribute_name)
        if isinstance(event_observer, TelegramEventObserver):
          logger.info(f"Registering event handler for event '{event}'")
          event_observer.register(partial(handler, activation, conversation.steps))
        else:
          raise NotImplementedError(f"Unsupported event type: {event}")
      case _:
        logger.warning("Unsupported activation type in context of Telegram bot: %s", type(activation))


def create_handlers(router: Router, conversation: Conversation) -> None:
  logger.info(f"Creating handler for conversation '{conversation.conversation_id}'")

  activate_entry_points(conversation, router)


def create(flow: Flow) -> Router:
  logger.info(f"Creating aiogram router for flow '{flow.name}'")
  router = Router(name=flow.name)
  for conversation in flow.conversations:
    create_handlers(router, conversation)

  return router
