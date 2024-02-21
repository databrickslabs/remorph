import logging
from datetime import timedelta

from databricks.labs.blueprint.installation import Installation
from databricks.labs.blueprint.tui import Prompts
from databricks.labs.blueprint.wheels import ProductInfo
from databricks.sdk import WorkspaceClient

from databricks.labs.remorph.__about__ import __version__
from databricks.labs.remorph.config import MorphConfig
from databricks.labs.remorph.install import WorkspaceInstallation

logger = logging.getLogger("databricks.labs.remorph.install")

PRODUCT_INFO = ProductInfo(__file__)

if __name__ == "__main__":
    logger.setLevel("INFO")
    ws = WorkspaceClient(product="remorph", product_version=__version__)
    current = Installation(ws, PRODUCT_INFO.product_name())
    config = current.load(MorphConfig)

    installer = WorkspaceInstallation(config, current, ws, Prompts(), timedelta(minutes=2))
    installer.uninstall()
