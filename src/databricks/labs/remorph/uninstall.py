import logging

from databricks.sdk import WorkspaceClient

from databricks.labs.remorph.__about__ import __version__
from databricks.labs.remorph.contexts.application import CliContext
from databricks.labs.remorph.deployment.dashboard import DashboardDeployment
from databricks.labs.remorph.deployment.installation import WorkspaceInstallation
from databricks.labs.remorph.deployment.job import JobDeployment
from databricks.labs.remorph.deployment.recon import ReconDeployment
from databricks.labs.remorph.deployment.table import TableDeployment

logger = logging.getLogger("databricks.labs.remorph.install")


def run(context: CliContext):
    logger.setLevel("INFO")
    installation = WorkspaceInstallation(
        context,
        ReconDeployment(
            context,
            TableDeployment(context),
            JobDeployment(context),
            DashboardDeployment(context),
        ),
    )
    installation.uninstall()
    logger.info("Uninstallation completed successfully.")


if __name__ == "__main__":
    app_context = CliContext(WorkspaceClient(product="remorph", product_version=__version__))
    run(app_context)
