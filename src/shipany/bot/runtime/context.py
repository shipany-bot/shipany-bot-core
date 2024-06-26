import logging
import typing as t
from contextlib import asynccontextmanager

import inject
from pydantic import BaseModel, ConfigDict, Field

from shipany.bot.providers.secrets import SecretsProvider

logger = logging.getLogger(__name__)


class RuntimeContext(BaseModel):
  secrets: t.Mapping[str, str] = Field(frozen=True, default_factory=dict)
  model_config = ConfigDict(extra="forbid", frozen=True)


@asynccontextmanager
async def runtime_context() -> t.AsyncIterator[RuntimeContext]:
  try:
    secrets_provider = inject.instance(SecretsProvider)
  except inject.InjectorException:  # pragma: no cover
    logger.warning(
      "SecretsProvider is not found in the injector. Have you forgotten to call default_runtime_injections?"
    )
    raise

  async with secrets_provider.snapshot() as snapshot:
    yield RuntimeContext(secrets=snapshot)
