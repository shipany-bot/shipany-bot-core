from __future__ import annotations

import typing as t

from pydantic_core import core_schema
from semver import Version

if t.TYPE_CHECKING:
  from pydantic import GetJsonSchemaHandler
  from pydantic.json_schema import JsonSchemaValue


class _VersionPydanticAnnotation:
  @classmethod
  def __get_pydantic_core_schema__(
    cls: type[t.Self],
    _source_type: t.Any,  # noqa: ANN401
    _handler: t.Callable[[t.Any], core_schema.CoreSchema],
  ) -> core_schema.CoreSchema:
    def validate_from_str(value: str) -> Version:
      return Version.parse(value)

    from_str_schema = core_schema.chain_schema(
      [
        core_schema.str_schema(),
        core_schema.no_info_plain_validator_function(validate_from_str),
      ]
    )

    return core_schema.json_or_python_schema(
      json_schema=from_str_schema,
      python_schema=core_schema.union_schema(
        [
          core_schema.is_instance_schema(Version),
          from_str_schema,
        ]
      ),
      serialization=core_schema.to_string_ser_schema(),
    )

  @classmethod
  def __get_pydantic_json_schema__(
    cls: type[t.Self], _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
  ) -> JsonSchemaValue:
    return handler(core_schema.str_schema())


ManifestVersion = t.Annotated[Version, _VersionPydanticAnnotation]
