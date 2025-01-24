import logging
import webbrowser
import yaml

from databricks.sdk import WorkspaceClient
from databricks.labs.blueprint.tui import Prompts
from databricks.labs.remorph.__about__ import __version__
from pathlib import Path

class ConfigureAssessment:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel("INFO")
        self.prompts = Prompts()

    def run(self):
        has_workspace = self.prompts.confirm("Do you have an existing Databricks workspace?")
        if not has_workspace:
            self.logger.info("Please create a Databricks workspace before proceeding.")
            raise SystemExit("Currently version of Remorph Assessment requires a Databricks workspace"
                             "Contact your Representive.")

        workspace_url = self.prompts.question("Please enter the Databricks workspace URL:")


        self.logger.info(f"Opened Databricks workspace URL: {workspace_url}")
        self.logger.info("Please follow the instructions to configure your access token or configure manually.")
        webbrowser.open(workspace_url)

        config_file_path = Path.home() / ".databrickscfg"
        with open(config_file_path, 'a', encoding='utf-8') as config_file:
            config_file.write("[remorph_assessment]\n")
            config_file.write(f"host = {workspace_url}\n")
            token = self.prompts.question("Please enter your Databricks access token:")
            config_file.write(f"token = {token}\n")
        try:
            "Tracking user agent"
            ws = WorkspaceClient(profile="remorph_assessment", product="remorph", product_version=__version__)
            self.logger.info(f"Successfully connected to the Databricks workspace. ${ws.current_user.me()}")
        except Exception as e:
            self.logger.error(f"Failed to connect to the Databricks workspace: {e}")
            raise SystemExit("Connection validation failed. Exiting...")

        # Step 6: Ask for source details and credentials
        source_details = self.prompts.question("Please enter the source details:")
        user_home = f"{Path(__file__).home()}"
        cred_file = Path(f"{user_home}/.databricks/labs/{self._product_info.product_name()}/credentials.yml")

        if not cred_file.exists():
            with open(cred_file, 'w', encoding='utf-8') as file:
                self.logger.debug(f"Created new credential file at {cred_file}")
        else:
            overwrite = self.prompts.confirm("Credential file exists. Do you want to overwrite it?")
            if not overwrite:
                self.logger.info("Reusing existing credential file.")
            else:
                with open(cred_file, 'w', encoding='utf-8') as file:
                    self.logger.info(f"Overwriting credential file at {cred_file}")

        # Step 2: Guide the user to documentation around what local vs env means.
        self.logger.info("Please refer to the documentation to understand the difference between local and env.")

        # Step 3: Based on user response, populate secret_vault_type and secret_vault_name.
        secret_vault_type = self.prompts.question("Enter secret vault type (local | databricks | env):")
        secret_vault_name = self.prompts.question("Enter secret vault name (or leave blank for none):")

        credentials = {
            "secret_vault_type": self.prompts.question("Enter secret vault type (local | databricks | env):"),
            "secret_vault_name": self.prompts.question("Enter secret vault name (or leave blank for none):"),
            "mssql": {
                "database": "DB_NAME",
                "driver": "ODBC Driver 18 for SQL Server",
                "server": "example_host",
                "port": None,
                "user": None,
                "password": None
            }
        }

        with open(cred_file, 'w', encoding='utf-8') as file:
            yaml.dump(credentials, file, default_flow_style=False)

            self.logger.debug("Credential template created for MSSQL.")



        self.logger.info("Source details and credentials received.")
