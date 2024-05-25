import typing as t


class SecretsProvider(t.Protocol):
  def dump(self: t.Self) -> t.Mapping[str, str]: ...
