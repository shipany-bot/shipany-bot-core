import typing as t

import pytest
from pydantic import JsonValue, TypeAdapter, ValidationError

from shipany.bot import jsonlogic as jl
from shipany.bot.conversation.context import conversation_context


@pytest.mark.parametrize(
  ("raw_logic", "setup_locals", "expected"),
  [
    ({"in": ["Hello", "Hello World!"]}, None, True),
    ({"in": ["Hello", ["Hello", "World!"]]}, None, True),
    ({"in": [1, [3, 2, 1]]}, None, True),
    ({"==": ["test", "test"]}, None, True),
    ({"==": [1, 1]}, None, True),
    ({"==": [[1, 2], [1, 2]]}, None, True),
    ({"==": [1, "1"]}, None, False),
    ({"==": [True, False]}, None, False),
    ({"or": [True, False]}, None, True),
    ({"and": [True, False]}, None, False),
    ({"and": [{"==": [1, 1]}, {"in": ["c", "abc"]}]}, None, True),
    ({"not": [True]}, None, False),
    ({"not": [{"==": [1, 1]}]}, None, False),
    ({"var": "a"}, {"a": "1"}, "1"),
    ({"==": [{"var": "a"}, "1"]}, {"a": "1"}, True),
    ({"var": "a"}, {"v": "2", "2": "a"}, ""),
    ({"in": [{"var": "a"}, ["3", "2", "1"]]}, {"a": "1"}, True),
    ({"==": ["hello", {"var": "text"}]}, {"text": "hello"}, True),
    ({"or": [{"==": ["hello", {"var": "text"}]}, {"==": ["hi", {"var": "text"}]}]}, {"text": "hello"}, True),
  ],
)
async def test_jsonlogic_rules_as_py_object(raw_logic: JsonValue, expected: JsonValue) -> None:
  async with conversation_context() as ctx:
    logic: jl.JsonLogic = t.cast(jl.JsonLogic, TypeAdapter(jl.JsonLogic).validate_python(raw_logic))
    assert jl.apply(logic, ctx) == expected


@pytest.mark.parametrize(
  ("string_logic", "setup_locals", "expected"),
  [
    ('{"in": ["Hello", "Hello World!"]}', None, True),
    ('{"in": ["Hello", ["Hello", "World!"]]}', None, True),
    ('{"in": [{"var": "a"}, ["Hello", "hi"]]}', {"a": "hi"}, True),
    ('{"in": [1, [3, 2, 1]]}', None, True),
    ('{"==": ["test", "test"]}', None, True),
    ('{"==": [1, 1]}', None, True),
    ('{"==": [[1, 2], [1, 2]]}', None, True),
    ('{"==": [1, "1"]}', None, False),
    ('{"==": [true, false]}', None, False),
    ('{"or": [true, false]}', None, True),
    ('{"and": [true, false]}', None, False),
    ('{"and": [{"==": [1, 1]}, {"in": ["c", "abc"]}]}', None, True),
    ('{"not": [true]}', None, False),
    ('{"not": [{"==": [1, 1]}]}', None, False),
    ('{"var": "a"}', {"a": "1"}, "1"),
    ('{"==": [{"var": "a"}, 1]}', {"a": "1"}, False),
    ('{"var": "a"}', {"v": "2", "2": "a"}, ""),
    ('{"in": [{"var": "a"}, ["3", "2", "1"]]}', {"a": "1"}, True),
    ('{"==": ["hello", {"var": "text"}]}', {"text": "hello"}, True),
    ('{"or": [{"==": ["hello", {"var": "text"}]}, {"==": ["hi", {"var": "text"}]}]}', {"text": "hello"}, True),
  ],
)
async def test_jsonlogic_rules_as_json_strings(string_logic: str, expected: JsonValue) -> None:
  async with conversation_context() as ctx:
    logic: jl.JsonLogic = t.cast(jl.JsonLogic, TypeAdapter(jl.JsonLogic).validate_json(string_logic))
    assert jl.apply(logic, ctx) == expected


@pytest.mark.parametrize(
  ("raw_logic", "logic_type"),
  [
    ('{"in": ["Hello"]}', jl.InOperation),
    ('{"==": ["test"]}', jl.EqualsOperation),
    ('{"or": [false]}', jl.OrOperation),
    ('{"and": [true]}', jl.AndOperation),
    ('{"not": [true, false]}', jl.NotOperation),
    ('{"var": 1}', jl.VarOperation),
  ],
)
def test_validation_error_raised_on_incomplete_data(raw_logic: str, logic_type: jl.JsonLogic) -> None:
  with pytest.raises(ValidationError):
    logic_type.model_validate_json(raw_logic)
