import logging
import webbrowser

from databricks.sdk import WorkspaceClient
from databricks.labs.blueprint.tui import Prompts
from databricks.labs.remorph import __version__


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
_DOC_URL = "https://docs.databricks.com/en/dev-tools/auth/pat.html"


class ConfigureAssessment:
    def __init__(self, product_name: str):
        self.prompts = Prompts()
        self._product_name = product_name

    def run(self):
        has_workspace = self.prompts.confirm("Do you have an existing Databricks workspace?")
        if not has_workspace:
            logger.info("Please create a Databricks workspace before proceeding.")
            raise SystemExit(
                "Current version of Remorph Assessment requires a Databricks workspace Contact your Account Rep."
            )

        workspace_url = self.prompts.question("Please enter the Databricks workspace URL")

        logger.info(f"Opened Databricks workspace URL: {workspace_url}")
        webbrowser.open(workspace_url)
        logger.info(f"Please follow the instructions to configure your access token {_DOC_URL}")
        webbrowser.open(_DOC_URL)
        logger.info("Please run the following command to configure your Databricks CLI profile")
        logger.info(f"databricks configure --profile remorph_assessment --host {workspace_url}")

        if not self.prompts.confirm("Confirm that you have created the profile"):
            logger.error("Please create the profile and try again.")
            raise SystemExit(
                "Current version of Remorph Assessment requires a Databricks workspace Contact your Account Rep."
            )

        try:
            # Tracking user agent
            ws = WorkspaceClient(profile="remorph_assessment", product=self._product_name, product_version=__version__)
            logger.info("Successfully connected to the Databricks workspace.")
            logger.debug(f"User Details: ${ws.current_user.me()}")
        except Exception as e:
            logger.error(f"Failed to connect to the Databricks workspace: {e}")
            raise SystemExit("Connection validation failed. Exiting...") from e

        # cred_manager = Credentials(self._product_name, EnvGetter(False))
        # cred_manager.configure(self.prompts)

        logger.info("Source details and credentials received.")
