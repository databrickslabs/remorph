import logging
import webbrowser
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
        """
        step 1 open .databrickscfg file in home directory
        step 2 add tag [remorph_assessment]
        step 3 add host = <workspace_url>
        step 4 add token = ask the user to paste the value here
        """

        try:
            ws = WorkspaceClient(profile="remorph_assessment", product="remorph", product_version=__version__)
            self.logger.info(f"Successfully connected to the Databricks workspace. ${ws.current_user.me()}")
        except Exception as e:
            self.logger.error(f"Failed to connect to the Databricks workspace: {e}")
            raise SystemExit("Connection validation failed. Exiting...")

        # Step 6: Ask for source details and credentials
        source_details = self.prompts.question("Please enter the source details:")
        credentials = self.prompts.question("Please enter your credentials:")
        user_home = f"{Path(__file__).home()}"
        Path(f"{user_home}/.databricks/labs/{self._product_info.product_name()}/credentials.yml")
        self.logger.info("Source details and credentials received.")
