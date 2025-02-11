import logging
import shutil
import yaml

from databricks.labs.blueprint.tui import Prompts

from databricks.labs.remorph.connections.credential_manager import cred_file as creds
from databricks.labs.remorph.connections.database_manager import DatabaseManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

PROFILER_SOURCE_SYSTEM = ["mssql"]


class ConfigureAssessment:
    def __init__(self, product_name: str, prompts: Prompts, credential_file=None):
        self.prompts = prompts
        self._product_name = product_name
        self._credential_file = creds(product_name) if not credential_file else credential_file

    def _configure_source_credentials(self):
        cred_file = self._credential_file
        source = str(
            self.prompts.choice("Please select the source system you want to configure", PROFILER_SOURCE_SYSTEM)
        ).lower()
        logger.info(
            "\n(local | env) \nlocal means values are read as plain text \nenv means values are read "
            "from environment variables fall back to plain text if not variable is not found\n",
        )
        secret_vault_type = str(self.prompts.choice("Enter secret vault type (local | env)", ["local", "env"])).lower()

        secret_vault_name = None

        # TODO Implement Databricks secret vault

        logger.info("Please refer to the documentation to understand the difference between local and env.")

        # Currently covering only MSSQL
        credential = {
            "secret_vault_type": secret_vault_type,
            "secret_vault_name": secret_vault_name,
            source: {
                "database": self.prompts.question("Enter the database name"),
                "driver": self.prompts.question("Enter the driver details"),
                "server": self.prompts.question("Enter the server or host details"),
                "port": int(self.prompts.question("Enter the port details", valid_number=True)),
                "user": self.prompts.question("Enter the user details"),
                "password": self.prompts.question("Enter the password details"),
            },
        }

        if cred_file.exists():
            backup_filename = cred_file.with_suffix('.bak')
            shutil.copy(cred_file, backup_filename)
            logger.debug(f"Backup of the existing file created at {backup_filename}")

        with open(cred_file, 'w', encoding='utf-8') as file:
            yaml.dump(credential, file, default_flow_style=False)

        logger.info(f"Credential template created for {source}.")

        return source

    @staticmethod
    def _test_connection(source: str, cred_manager):
        config = cred_manager.load(source)

        try:
            db_manager = DatabaseManager(source, config)
            if db_manager.check_connection():
                logger.info("Connection to the source system successful")
            else:
                logger.error("Connection to the source system failed, check logs in debug mode")
                raise SystemExit("Connection validation failed. Exiting...")

        except ConnectionError as e:
            logger.error(f"Failed to connect to the source system: {e}")
            raise SystemExit("Connection validation failed. Exiting...") from e

    def run(self, cred_manager=None):
        logger.info("Welcome to the Remorph Assessment Configuration")
        source = self._configure_source_credentials()
        logger.info("Source details and credentials received.")
        if self.prompts.confirm("Do you want to test the connection to the source system?"):
            self._test_connection(source, cred_manager)

        logger.info("Remorph Assessment Configuration Completed")
        # TODO Add the instructions for next step
        # logger.info("You can now Remorph Assessment Execute command to start the assessment")
