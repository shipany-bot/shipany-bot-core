from __future__ import annotations

import json
import logging
import typing as t

from jsonpath_ng import jsonpath, parse

from shipany.bot.contrib.aiogram.action_dispatcher import GoToNextAction
from shipany.bot.contrib.aiogram.context import Context
from shipany.bot.contrib.aiogram.renders.jinja_env import template_from_context

if t.TYPE_CHECKING:
  from shipany.bot.actions.json_path_action.v1 import JsonPathAction
  from shipany.bot.contrib.aiogram.context import Context

logger = logging.getLogger(__name__)


def process(ctx: Context, action: JsonPathAction) -> GoToNextAction:
  if not action.captures:
    return GoToNextAction()

  value = template_from_context(action.input_, ctx)
  jsonpath_expr: jsonpath.Child = parse(action.expression)
  try:
    json_value = json.loads(value)
    matches: list[jsonpath.DatumInContext] = jsonpath_expr.find(json_value)
    for key, match_ in zip(action.captures.keys(), matches):
      ctx.captures[key] = json.dumps(match_.value if match_ is not None else None)
  except json.JSONDecodeError as e:
    logger.exception(f"Error while parsing JSON: {e}", exc_info=False)  # noqa: TRY401
    pass
  return GoToNextAction()
