import json
import os

from databricks.connect import DatabricksSession
from databricks.labs.blueprint.entrypoint import get_logger
from databricks.labs.blueprint.tui import Prompts
from databricks.sdk import WorkspaceClient

from databricks.labs.remorph.helpers.db_workspace_utils import DatabricksSecretsClient
from databricks.labs.remorph.reconcile.connectors.data_source_factory import (
    DataSourceFactory,
)
from databricks.labs.remorph.reconcile.constants import SourceType
from databricks.labs.remorph.reconcile.recon_config import TableRecon

logger = get_logger(__file__)

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
                raise SystemExit(f"Source {self._source} is not yet configured...")

    def prompt_and_save_connection_details(self):
        """
        Prompt for connection details and save them as Secrets in Databricks Workspace
        """
        # prompt for connection_details only if source is other than Databricks
        if self._source == SourceType.DATABRICKS.value:
            logger.info("*Databricks* as a source is supported only for **Hive MetaStore (HMS) setup**")
            return

        # Prompt for secret scope
        scope_name = self._prompts.question("Enter Scope name")
        self._db_secrets.get_or_create_scope(scope_name)

        # Prompt for connection details
        connection_details = self._connection_details()
        logger.debug(f"Storing `{self._source}` connection details as Secrets in Databricks Workspace...")
        self._db_secrets.store_connection_secrets(scope_name, connection_details)

    def _prompt_catalog_schema(self) -> dict[str, str]:
        """
        Prompt for source, target catalog and schema names
        :return:
        """
        src_catalog_name = None
        src_schema_prompt = f"Enter `{self._source}` schema_name"

        # Prompt for `catalog_name` only if source is snowflake
        if self._source in {SourceType.SNOWFLAKE.value}:
            src_catalog_name = self._prompts.question(f"Enter `{self._source}` catalog_name")
            src_schema_prompt = f"Enter `{self._source}` database_name"

        src_schema_name = self._prompts.question(src_schema_prompt)

        tgt_catalog_name = self._prompts.question("Enter target catalog_name")
        tgt_schema_name = self._prompts.question("Enter target schema_name")

        return {
            "src_catalog": src_catalog_name,
            "src_schema": src_schema_name,
            "tgt_catalog": tgt_catalog_name,
            "tgt_schema": tgt_schema_name,
        }

    def _confirm_secret_scope(self):
        if not self._prompts.confirm(f"Did you setup the secrets for the `{self._source}` connection?"):
            raise ValueError(
                f"Error: Secrets are needed for `{self._source}` reconciliation."
                f"\nUse `remorph configure-secrets` to setup Scope and Secrets."
            )

    def _prompt_config_details(self) -> TableRecon:
        """
        Prompt for Scope, source, target catalog and schema names. Get the table list and return the TableRecon config
        :return: TableRecon
        """
        # Prompt for secret scope
        secret_scope = self._prompts.question("Enter Secret Scope name")

        self._db_secrets.get_or_create_scope(secret_scope)

        # Prompt for catalog and schema
        catalog_schema_dict = self._prompt_catalog_schema()
        spark = DatabricksSession.builder.getOrCreate()

        only_subset = self._prompts.confirm("Do you want to include/exclude a set of tables?")
        include_list = []
        exclude_list = []

        if only_subset:
            # Prompt for filter
            filter_types = ["include", "exclude"]
            filter_type = self._prompts.choice("Select the filter type", filter_types)
            subset_tables = self._prompts.question(f"Enter the tables(separated by comma) to `{filter_type}`")
            subset_tables = [f"'{table.strip().upper()}'" for table in subset_tables.split(",")]

            include_list = subset_tables if filter_type == "include" else None
            exclude_list = subset_tables if filter_type == "exclude" else None

        # Get DataSource
        data_source = DataSourceFactory.get_data_source(self._source, spark, self._db_secrets.ws, secret_scope)
        logger.debug(f"Listing tables for `{self._source}` using DataSource")
        # Get TableRecon config
        recon_config = data_source.list_tables(
            catalog_schema_dict.get("src_catalog"), catalog_schema_dict.get("src_schema"), include_list, exclude_list
        )

        # Update the target catalog and schema
        recon_config.target_catalog = catalog_schema_dict.get("tgt_catalog")
        recon_config.target_schema = catalog_schema_dict.get("tgt_schema")
        logger.info(f"Recon Config details are fetched successfully...{recon_config}")

        return recon_config

    def _save_config_details(self, recon_config_json):
        """
        Save the config details in a file
        """
        recon_conf_abspath = os.path.abspath(f"./recon_conf_{self._source}.json")
        logger.debug(f"Saving the config details for `{self._source}` in `{recon_conf_abspath}` file")
        with open(f"./recon_conf_{self._source}.json", "w", encoding="utf-8") as f:
            exit_code = f.write(recon_config_json)
            logger.debug(f"File written, exit_code {exit_code}")
        logger.info(f"Config details are saved at path: `{recon_conf_abspath}`")

    def prompt_and_save_config_details(self):
        """
        Prompt for source, target catalog and schema names. Get the table list and save the config details
        """
        # Check for Secrets Scope
        self._confirm_secret_scope()
        recon_config = self._prompt_config_details()
        recon_config_json = json.dumps(recon_config, default=vars, indent=2, sort_keys=True)
        recon_config_json_formatted = recon_config_json.replace("null", "None")
        logger.debug(f"recon_config_json : {recon_config_json_formatted}")

        self._save_config_details(recon_config_json_formatted)
