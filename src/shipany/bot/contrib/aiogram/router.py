from __future__ import annotations

import logging
import typing as t
from functools import partial

from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.dispatcher.router import Router
from aiogram.filters.command import Command

from shipany.bot.contrib.aiogram.context import persistent_context
from shipany.bot.contrib.aiogram.events.handler import AiogramEventHandler
from shipany.bot.contrib.aiogram.renders.context_proxy import proxy
from shipany.bot.conversation.v1.models import (
  CommandActivation,
  Conversation,
  EventActivation,
  Flow,
)
from shipany.bot.jsonlogic import apply

if t.TYPE_CHECKING:
  from aiogram.methods import TelegramMethod
  from aiogram.types import TelegramObject

  from shipany.bot.conversation.v1.models.activations import Activation
  from shipany.bot.conversation.v1.models.steps import Steps

logger = logging.getLogger(__name__)


async def handler(activation: Activation, steps: Steps, event: TelegramObject) -> TelegramMethod | None:
  context = persistent_context.model_copy(update={"event": event})
  if activation.condition is not None:
    logger.info("Checking condition %s", activation.condition)
    if not apply(activation.condition, proxy(context)):
      logger.info("The condition is not met. Skipping the handler.")
      raise SkipHandler

  wrapper = AiogramEventHandler(steps, begin_with_step_id=activation.next_step)
  return await wrapper(context)


def activate_entry_points(conversation: Conversation, router: Router) -> None:
  for activation in conversation.activations:
    # aiogram cannot recognize callable objects, so we need to wrap the handler in a function

    if isinstance(activation, CommandActivation):
      logger.info(f"Registering command handler for command '{activation.command}'")
      router.message.register(partial(handler, activation, conversation.steps), Command(activation.command))

    elif isinstance(activation, EventActivation):
      mapping = {
        "on-message": router.message,
        "on-edited-message": router.edited_message,
        "on-channel-post": router.channel_post,
        "on-edited-channel-post": router.edited_channel_post,
        "on-inline-query": router.inline_query,
        "on-chosen-inline-result": router.chosen_inline_result,
        "on-callback-query": router.callback_query,
        "on-shipping-query": router.shipping_query,
        "on-pre-checkout-query": router.pre_checkout_query,
        "on-poll": router.poll,
        "on-poll-answer": router.poll_answer,
        "on-my-chat-member": router.my_chat_member,
        "on-chat-member": router.chat_member,
        "on-chat-join-request": router.chat_join_request,
        "on-message-reaction": router.message_reaction,
        "on-message-reaction-count": router.message_reaction_count,
        "on-chat-boost": router.chat_boost,
        "on-removed-chat-boost": router.removed_chat_boost,
      }
      if (event_observer := mapping.get(activation.event)) is not None:
        logger.info(f"Registering event handler for event '{activation.event}'")
        event_observer.register(partial(handler, activation, conversation.steps))
      else:
        raise NotImplementedError(f"Unsupported event type: {activation.event}")
    else:
      raise NotImplementedError(f"Unsupported activation type: {type(activation)}")


def create_handlers(router: Router, conversation: Conversation) -> None:
  logger.info(f"Creating handler for conversation '{conversation.conversation_id}'")

  activate_entry_points(conversation, router)


def create(flow: Flow) -> Router:
  logger.info(f"Creating aiogram router for flow '{flow.name}'")
  router = Router(name=flow.name)
  for conversation in flow.conversations:
    create_handlers(router, conversation)

  return router
