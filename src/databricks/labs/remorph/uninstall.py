import logging

from databricks.sdk import WorkspaceClient

from databricks.labs.remorph.__about__ import __version__
from databricks.labs.remorph.install import WorkspaceInstallation

logger = logging.getLogger("databricks.labs.remorph.install")

if __name__ == "__main__":
    logger.setLevel("INFO")
    ws = WorkspaceClient(product="remorph", product_version=__version__)
    installer = WorkspaceInstallation.current(ws)
    installer.uninstall()
