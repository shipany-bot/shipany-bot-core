from __future__ import annotations

import logging
import typing as t

from shipany.bot import jsonlogic as jl

if t.TYPE_CHECKING:
  from pydantic import JsonValue

T = t.TypeVar("T")
RenderFunction = t.Callable[[t.Iterable[T]], t.Iterable[T]]
logger = logging.getLogger(__name__)


class SupportsGetOrDefault(t.Protocol):
  def __getitem__(self: t.Self, key: str, /) -> JsonValue: ...


def apply(logic: jl.JsonLogic, data: SupportsGetOrDefault) -> JsonValue:
  logger.info("Applying logic: %s", logic)
  match logic:
    case jl.InOperation(args=args):
      arg0 = apply(args[0], data) if isinstance(args[0], jl.JsonLogic) else args[0]  # type: ignore[has-type]
      arg1 = apply(args[1], data) if isinstance(args[1], jl.JsonLogic) else args[1]  # type: ignore[has-type]
      return arg0 in arg1
    case jl.EqualsOperation(args=args):
      iterator: t.Iterator[
        jl.EqualsOperation
        | jl.InOperation
        | jl.AndOperation
        | jl.OrOperation
        | jl.NotOperation
        | jl.VarOperation
        | str
        | int
        | bool
        | float
        | list[str | int | bool | float]
      ] = iter(args)  # type: ignore[has-type]
      first = next(iterator)
      if isinstance(first, jl.JsonLogic):
        first = apply(first, data)
      return all(first == (apply(x, data) if isinstance(x, jl.JsonLogic) else x) for x in iterator)
    case jl.AndOperation(args=args):
      return all(
        apply(sub_logic, data) if isinstance(sub_logic, jl.JsonLogic) else sub_logic
        for sub_logic in args  # type: ignore[has-type]
      )
    case jl.OrOperation(args=args):
      return any(
        apply(sub_logic, data) if isinstance(sub_logic, jl.JsonLogic) else sub_logic
        for sub_logic in args  # type: ignore[has-type]
      )
    case jl.NotOperation(args=args):
      return not apply(args[0], data) if isinstance(args[0], jl.JsonLogic) else not args[0]  # type: ignore[has-type]
    case jl.VarOperation(var=var):
      try:
        return data[var]  # type: ignore[has-type]
      except KeyError:
        logger.warning("Variable %s not found in data. Returning None", var)  # type: ignore[has-type]
        return None
  t.assert_never(logic)
