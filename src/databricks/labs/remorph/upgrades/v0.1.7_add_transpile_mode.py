# pylint: disable=invalid-name

import logging

from databricks.labs.blueprint.installation import Installation
from databricks.sdk import WorkspaceClient

from databricks.labs.remorph.config import MorphConfig

logger = logging.getLogger(__name__)


def upgrade(installation: Installation, _: WorkspaceClient):
    config = installation.load(MorphConfig)

    installation.save(config)
