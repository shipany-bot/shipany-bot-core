from __future__ import annotations

from .models.flow import Flow
from .models.validators import all_checks


def _validate(flow: Flow) -> None:
  for check in all_checks:
    check(flow)


def load(json_data: str | bytes | bytearray) -> Flow:
  model = Flow.model_validate_json(json_data)
  _validate(model)
  return model
