# mypy: disable-error-code="has-type"
from __future__ import annotations

import typing as t

from aiogram import types

from shipany.bot.persistency.handles import HandleGenerator
from shipany.bot.providers.captures import Scope


class EventInspector:
  def __init__(self: t.Self, event: types.TelegramObject) -> None:
    self._event = event

  def user_id(self: t.Self) -> str:
    match self._event:
      case types.Message(from_user=types.User(id=user_id)):
        return str(user_id)
      case types.MessageReactionUpdated(user=types.User(id=user_id)):
        return str(user_id)
    raise NotImplementedError(f"Can't extract user id from {self._event!r}")

  def chat_id(self: t.Self) -> str:
    match self._event:
      case types.Message(chat=types.Chat(id=chat_id)):
        return str(chat_id)
      case types.MessageReactionUpdated(chat=types.Chat(id=chat_id)):
        return str(chat_id)
    raise NotImplementedError(f"Can't extract chat id from {self._event!r}")


class AiogramHandleGenerator(HandleGenerator):
  def __init__(self: t.Self, event: t.Any) -> None:  # noqa: ANN401
    if not isinstance(event, types.TelegramObject):
      raise TypeError(f"Expected TelegramObject, got {event!r}")

    self._event_inspector = EventInspector(event)

  def generate(self: t.Self, key: str, scope: list[Scope]) -> str:
    return ":".join(
      [
        self._event_inspector.user_id() if Scope.user in scope else "_",
        self._event_inspector.chat_id() if Scope.chat in scope else "_",
        key,
      ]
    )


class HandleGeneratorFactory:
  def create(self: t.Self, event: t.Any) -> HandleGenerator:  # noqa: ANN401
    return AiogramHandleGenerator(event)
