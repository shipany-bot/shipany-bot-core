from __future__ import annotations

import typing as t

from pydantic import BaseModel, ConfigDict, Field, model_validator

from shipany.bot.persistency.scopes import Scope  # noqa: TCH001


class EqualsOperation(BaseModel):
  args: list[JsonLogic | str | int | bool | float | list[str | int | bool | float]] = Field(alias="==")
  model_config = ConfigDict(frozen=True, extra="forbid")

  @model_validator(mode="after")
  def check_args_length(self: t.Self) -> t.Self:
    if len(self.args) < 2:
      raise ValueError(f"Expected at least 2 arguments, got {len(self.args)}")
    return self


class InOperation(BaseModel):
  args: list[JsonLogic | str | int | bool | float | list[str | int | bool | float]] = Field(alias="in")
  model_config = ConfigDict(frozen=True, extra="forbid")

  @model_validator(mode="after")
  def check_args_length(self: t.Self) -> t.Self:
    if len(self.args) != 2:
      raise ValueError(f"Expected 2 arguments, got {len(self.args)}")
    return self


class AndOperation(BaseModel):
  args: list[JsonLogic | str | int | bool | float] = Field(alias="and")
  model_config = ConfigDict(frozen=True, extra="forbid")

  @model_validator(mode="after")
  def check_args_length(self: t.Self) -> t.Self:
    if len(self.args) < 2:
      raise ValueError(f"Expected at least 2 arguments, got {len(self.args)}")
    return self


class OrOperation(BaseModel):
  args: list[JsonLogic | str | int | bool | float] = Field(alias="or")
  model_config = ConfigDict(frozen=True, extra="forbid")

  @model_validator(mode="after")
  def check_args_length(self: t.Self) -> t.Self:
    if len(self.args) < 2:
      raise ValueError(f"Expected at least 2 arguments, got {len(self.args)}")
    return self


class NotOperation(BaseModel):
  args: list[JsonLogic | str | int | bool | float] = Field(alias="not")
  model_config = ConfigDict(frozen=True, extra="forbid")

  @model_validator(mode="after")
  def check_args_length(self: t.Self) -> t.Self:
    if len(self.args) != 1:
      raise ValueError(f"Expected 1 argument, got {len(self.args)}")
    return self


class VarOperation(BaseModel):
  var: str = Field(alias="var", min_length=1)
  scope: Scope | None = None
  model_config = ConfigDict(frozen=True, extra="forbid")


JsonLogic = t.Union[EqualsOperation, InOperation, AndOperation, OrOperation, NotOperation, VarOperation]
