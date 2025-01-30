import logging
import webbrowser
from time import sleep

from databricks.sdk import WorkspaceClient
from databricks.labs.blueprint.tui import Prompts
from databricks.labs.remorph import __version__
from databricks.labs.remorph.connections.credential_manager import Credentials
from databricks.labs.remorph.connections.database_manager import DatabaseManager
from databricks.labs.remorph.connections.env_getter import EnvGetter

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
_DOC_URL = "https://docs.databricks.com/en/dev-tools/auth/pat.html"


class ConfigureAssessment:
    def __init__(self, product_name: str):
        self.prompts = Prompts()
        self._product_name = product_name

    def run(self):
        has_workspace = bool(self.prompts.choice("Do you have an existing Databricks workspace?", ["Yes", "No"]))
        if not has_workspace:
            logger.info("Please create a Databricks workspace before proceeding.")
            raise SystemExit(
                "Current version of Remorph Assessment requires a Databricks workspace Contact your Account Rep."
            )

        workspace_url = self.prompts.question("Please enter the Databricks workspace host")

        logger.info(f"Opened Databricks workspace host: {workspace_url}")
        webbrowser.open(workspace_url)
        sleep(3)  # Added this sleep for better transition
        logger.info(f"Please follow the instructions to configure your access token {_DOC_URL}")
        webbrowser.open(_DOC_URL)
        sleep(3)  # Added sleep for better transition
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

        cred_manager = Credentials(self._product_name, EnvGetter(False))
        source = cred_manager.configure(self.prompts)

        if self.prompts.confirm("Do you test the connection to the source system?"):
            config = cred_manager.load(source)
            try:
                db_manager = DatabaseManager("mssql", config)
                query = "SELECT 101 AS test_column"
                result = db_manager.execute_query(query)
                row = result.fetchone()
                assert row[0] == 101
                logger.info("Successfully connected to the source system.")
            except ConnectionError as e:
                logger.error(f"Failed to connect to the source system: {e}")
                raise SystemExit("Connection validation failed. Exiting...") from e

        logger.info("Source details and credentials received.")
