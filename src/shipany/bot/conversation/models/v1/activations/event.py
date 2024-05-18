from enum import StrEnum

from pydantic import Field

from .base import BaseActivation


class EventName(StrEnum):
  ON_MESSAGE = "on-message"
  ON_EDITED_MESSAGE = "on-edited-message"
  ON_CHANNEL_POST = "on-channel-post"
  ON_EDITED_CHANNEL_POST = "on-edited-channel-post"
  ON_INLINE_QUERY = "on-inline-query"
  ON_CHOSEN_INLINE_RESULT = "on-chosen-inline-result"
  ON_CALLBACK_QUERY = "on-callback-query"
  ON_SHIPPING_QUERY = "on-shipping-query"
  ON_PRE_CHECKOUT_QUERY = "on-pre-checkout-query"
  ON_POLL = "on-poll"
  ON_POLL_ANSWER = "on-poll-answer"
  ON_MY_CHAT_MEMBER = "on-my-chat-member"
  ON_CHAT_MEMBER = "on-chat-member"
  ON_CHAT_JOIN_REQUEST = "on-chat-join-request"
  ON_MESSAGE_REACTION = "on-message-reaction"
  ON_MESSAGE_REACTION_COUNT = "on-message-reaction-count"
  ON_CHAT_BOOST = "on-chat-boost"
  ON_REMOVED_CHAT_BOOST = "on-removed"


class EventActivation(BaseActivation):
  """Describes an event that triggers the conversation. Commonly used for message events."""

  event: EventName = Field(
    description="List of supported event names that can trigger the conversation steps.",
  )
