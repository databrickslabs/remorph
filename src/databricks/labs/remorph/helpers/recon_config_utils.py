import logging

from databricks.labs.blueprint.tui import Prompts
from databricks.sdk import WorkspaceClient

from databricks.labs.remorph.helpers.db_workspace_utils import DatabricksSecretsClient
from databricks.labs.remorph.reconcile.constants import SourceType

logger = logging.getLogger(__name__)

recon_source_choices = [
    SourceType.SNOWFLAKE.value,
    SourceType.ORACLE.value,
    SourceType.DATABRICKS.value,
    SourceType.NETEZZA.value,
]


class ReconConfigPrompts:
    def __init__(self, ws: WorkspaceClient, prompts: Prompts = Prompts()):
        self._source = None
        self._prompts = prompts
        self._db_secrets = DatabricksSecretsClient(ws, prompts)

    def prompt_source(self):
        source = self._prompts.choice("Select the source", recon_source_choices)
        self._source = source
        return source

    def _prompt_snowflake_connection_details(self) -> tuple[str, dict[str, str]]:
        """
        Prompt for Snowflake connection details
        :return: tuple[str, dict[str, str]]
        """
        logger.info(
            f"Please answer a couple of questions to configure `{SourceType.SNOWFLAKE.value}` Connection profile"
        )

        sf_url = self._prompts.question("Enter Snowflake URL")
        account = self._prompts.question("Enter Account Name")
        sf_user = self._prompts.question("Enter User")
        sf_password = self._prompts.question("Enter Password")
        sf_db = self._prompts.question("Enter Database")
        sf_schema = self._prompts.question("Enter Schema")
        sf_warehouse = self._prompts.question("Enter Snowflake Warehouse")
        sf_role = self._prompts.question("Enter Role", default=" ")

        sf_conn_details = {
            "sfUrl": sf_url,
            "account": account,
            "sfUser": sf_user,
            "sfPassword": sf_password,
            "sfDatabase": sf_db,
            "sfSchema": sf_schema,
            "sfWarehouse": sf_warehouse,
            "sfRole": sf_role,
        }

        sf_conn_dict = (SourceType.SNOWFLAKE.value, sf_conn_details)
        return sf_conn_dict

    def _prompt_oracle_connection_details(self) -> tuple[str, dict[str, str]]:
        """
        Prompt for Oracle connection details
        :return: tuple[str, dict[str, str]]
        """
        logger.info(f"Please answer a couple of questions to configure `{SourceType.ORACLE.value}` Connection profile")
        user = self._prompts.question("Enter User")
        password = self._prompts.question("Enter Password")
        host = self._prompts.question("Enter host")
        port = self._prompts.question("Enter port")
        database = self._prompts.question("Enter database/SID")

        oracle_conn_details = {"user": user, "password": password, "host": host, "port": port, "database": database}

        oracle_conn_dict = (SourceType.ORACLE.value, oracle_conn_details)
        return oracle_conn_dict

    def _connection_details(self):
        """
        Prompt for connection details based on the source
        :return: None
        """
        logger.debug(f"Prompting for `{self._source}` connection details")
        match self._source:
            case SourceType.SNOWFLAKE.value:
                return self._prompt_snowflake_connection_details()
            case SourceType.ORACLE.value:
                return self._prompt_oracle_connection_details()
            case _:
                raise ValueError(f"Source {self._source} is not yet configured...")

    def prompt_and_save_connection_details(self):
        """
        Prompt for connection details and save them as Secrets in Databricks Workspace
        """
        # prompt for connection_details only if source is other than Databricks
        if self._source == SourceType.DATABRICKS.value:
            logger.info("*Databricks* as a source is supported only for **Hive MetaStore (HMS) setup**")
            return

        # Prompt for secret scope
        scope_name = self._prompts.question("Enter Secret Scope name")
        self._db_secrets.get_or_create_scope(scope_name)

        # Prompt for connection details
        connection_details = self._connection_details()
        logger.debug(f"Storing `{self._source}` connection details as Secrets in Databricks Workspace...")
        self._db_secrets.store_connection_secrets(scope_name, connection_details)
