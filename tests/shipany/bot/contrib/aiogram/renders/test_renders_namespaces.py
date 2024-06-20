from __future__ import annotations

import typing as t

import pytest

from shipany.bot.contrib.aiogram.renders import namespaces
from shipany.bot.conversation.context import ConversationContext, conversation_context

if t.TYPE_CHECKING:
  from argparse import Namespace


@pytest.mark.parametrize(
  "namespace_func",
  [
    namespaces.message_namespace,
    namespaces.user_namespace,
    namespaces.reaction_namespace,
  ],
)
def test_another_event(namespace_func: t.Callable[[ConversationContext], Namespace | None]) -> None:
  with conversation_context() as ctx:
    assert namespace_func(ctx) is None
