import logging
import os

from databricks.labs.blueprint.installation import Installation

logger = logging.getLogger(__name__)


class DeploymentMixin:
    def name_prefix(self, name: str, installation: Installation) -> str:
        prefix = os.path.basename(installation.install_folder()).removeprefix('.')
        return f"[{prefix.upper()}] {name}"
