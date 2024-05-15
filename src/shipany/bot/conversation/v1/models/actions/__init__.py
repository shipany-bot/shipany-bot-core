from __future__ import annotations

import typing as t

from .base import BaseAction as BaseAction
from .function import FunctionAction as FunctionAction
from .message import MessageAction as MessageAction, SupportedMessageActionTypes as SupportedMessageActionTypes
from .state import StateAction as StateAction
from .transition import TransitionAction as TransitionAction

ActionType: t.TypeAlias = MessageAction | TransitionAction | FunctionAction | StateAction
ActionTypes = list[ActionType]
