import logging
import webbrowser

from databricks.labs.remorph.config import RemorphConfigs
from databricks.labs.remorph.connections.credential_manager import Credentials
from databricks.labs.remorph.connections.env_getter import EnvGetter
from databricks.sdk import WorkspaceClient
from databricks.labs.blueprint.tui import Prompts
from databricks.labs.blueprint.wheels import ProductInfo
from pathlib import Path


logger = logging.getLogger(__name__)


class ConfigureAssessment:
    def __init__(self):
        self.prompts = Prompts()

    def run(self):
        has_workspace = self.prompts.confirm("Do you have an existing Databricks workspace?")
        if not has_workspace:
            logger.info("Please create a Databricks workspace before proceeding.")
            raise SystemExit(
                "Currently version of Remorph Assessment requires a Databricks workspace" "Contact your Representive."
            )

        workspace_url = self.prompts.question("Please enter the Databricks workspace URL:")

        logger.info(f"Opened Databricks workspace URL: {workspace_url}")
        logger.info("Please follow the instructions to configure your access token or configure manually.")
        webbrowser.open(workspace_url)

        config_file_path = Path.home() / ".databrickscfg"
        with open(config_file_path, 'a', encoding='utf-8') as config_file:
            config_file.write("[remorph_assessment]\n")
            config_file.write(f"host = {workspace_url}\n")
            token = self.prompts.question("Please enter your Databricks access token:")
            config_file.write(f"token = {token}\n")

        product_info = ProductInfo.from_class(RemorphConfigs)
        try:
            "Tracking user agent"
            ws = WorkspaceClient(
                profile="remorph_assessment",
                product=product_info.product_name(),
                product_version=product_info.version(),
            )
            logger.info(f"Successfully connected to the Databricks workspace. ${ws.current_user.me()}")
        except Exception as e:
            logger.error(f"Failed to connect to the Databricks workspace: {e}")
            raise SystemExit("Connection validation failed. Exiting...")

        cred_manager = Credentials(product_info, EnvGetter(False))

        logger.info("Source details and credentials received.")
