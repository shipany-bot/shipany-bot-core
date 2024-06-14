# mypy: disable-error-code="has-type"
from __future__ import annotations

import json
import typing as t
from argparse import Namespace  # provides dot access to the attributes

import httpx

if t.TYPE_CHECKING:
  from shipany.bot.conversation.context import ConversationContext


def response_namespace(ctx: ConversationContext) -> Namespace | None:
  match ctx.event:
    case httpx.Response(status_code=status_code, text=text, headers=headers):
      return Namespace(
        status_code=str(status_code),
        text=text,
        headers=json.dumps(headers.multi_items()),
      )
  return None
