import logging

from databricks.labs.blueprint.tui import Prompts
from databricks.labs.remorph.connections.credential_manager import Credentials
from databricks.labs.remorph.connections.database_manager import DatabaseManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ConfigureAssessment:
    def __init__(self, product_name: str, prompts: Prompts, cred_manager: Credentials):
        self.prompts = prompts
        self._product_name = product_name
        self.cred_manager = cred_manager

    def _configure_source_credentials(self):
        source = self.cred_manager.configure(self.prompts)

        if self.prompts.confirm("Do you test the connection to the source system?"):
            config = self.cred_manager.load(source)
            try:
                db_manager = DatabaseManager(source, config)
                db_manager.connection_test()
            except ConnectionError as e:
                logger.error(f"Failed to connect to the source system: {e}")
                raise SystemExit("Connection validation failed. Exiting...") from e

        logger.info("Source details and credentials received.")

    def run(self):
        logger.info("Welcome to the Remorph Assessment Configuration")
        self._configure_source_credentials()
        logger.info("Remorph Assessment Configuration Completed")
        # TODO Add the instructions for next step
        # logger.info("You can now Remorph Assessment Execute command to start the assessment")
