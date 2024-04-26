import json
import logging
import webbrowser

from databricks.connect import DatabricksSession
from databricks.labs.blueprint.installation import Installation
from databricks.labs.blueprint.tui import Prompts
from databricks.labs.blueprint.wheels import ProductInfo

from databricks.labs.remorph.__about__ import __version__
from databricks.labs.remorph.reconcile.constants import SourceType
from databricks.labs.remorph.config import TableRecon, get_data_source
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors.platform import ResourceDoesNotExist

from ..config import get_data_source

PRODUCT_INFO = ProductInfo(__file__)

logger = logging.getLogger(__name__)

recon_source_choices = [
    SourceType.SNOWFLAKE.value,
    SourceType.ORACLE.value,
    SourceType.DATABRICKS.value,
]


class ReconConfigPrompts:
    def __init__(self, ws: WorkspaceClient, prompts: Prompts = Prompts()):
        self._source = None
        self._prompts = prompts
        self._ws = ws

    def _scope_exists(self, scope_name: str) -> bool:
        scope_exists = scope_name in [scope.name for scope in self._ws.secrets.list_scopes()]

        if not scope_exists:
            logger.error(
                f"Error: Cannot find Secret Scope: `{scope_name}` in Databricks Workspace."
                f"\nUse `remorph configure-secrets` to setup Scope and Secrets"
            )
            return False
        logger.debug(f"Found Scope: `{scope_name}` in Databricks Workspace")
        return True

    def _ensure_scope_exists(self, scope_name: str):
        """
        Get or Create a new Scope in Databricks Workspace
        :param scope_name:
        """
        scope_exists = self._scope_exists(scope_name)
        if not scope_exists:
            allow_scope_creation = self._prompts.confirm("Do you want to create a new one?")
            if not allow_scope_creation:
                msg = "Scope is needed to store Secrets in Databricks Workspace"
                raise SystemExit(msg)

            try:
                logger.debug(f" Creating a new Scope: `{scope_name}`")
                self._ws.secrets.create_scope(scope_name)
            except Exception as ex:
                logger.error(f"Exception while creating Scope `{scope_name}`: {ex}")
                raise ex

            logger.info(f" Created a new Scope: `{scope_name}`")
        logger.info(f" Using Scope: `{scope_name}`...")

    def _secret_key_exists(self, scope_name: str, secret_key: str) -> bool:
        try:
            self._ws.secrets.get_secret(scope_name, secret_key)
            logger.info(f"Found Secret key `{secret_key}` in Scope `{scope_name}`")
            return True
        except ResourceDoesNotExist:
            logger.debug(f"Secret key `{secret_key}` not found in Scope `{scope_name}`")
            return False

    def _store_secret(self, scope_name: str, secret_key: str, secret_value: str):
        try:
            logger.debug(f"Storing Secret: *{secret_key}* in Scope: `{scope_name}`")
            self._ws.secrets.put_secret(scope=scope_name, key=secret_key, string_value=secret_value)
        except Exception as ex:
            logger.error(f"Exception while storing Secret `{secret_key}`: {ex}")
            raise ex

    def store_connection_secrets(self, scope_name: str, conn_details: tuple[str, dict[str, str]]):
        engine = conn_details[0]
        secrets = conn_details[1]

        logger.debug(f"Storing `{engine}` Connection Secrets in Scope: `{scope_name}`")

        for key, value in secrets.items():
            secret_key = engine + '_' + key
            logger.debug(f"Processing Secret: *{secret_key}*")
            debug_op = "Storing"
            info_op = "Stored"
            if self._secret_key_exists(scope_name, secret_key):
                overwrite_secret = self._prompts.confirm(f"Do you want to overwrite `{secret_key}`?")
                if not overwrite_secret:
                    continue
                debug_op = "Overwriting"
                info_op = "Overwritten"

            logger.debug(f"{debug_op} Secret: *{secret_key}* in Scope: `{scope_name}`")
            self._store_secret(scope_name, secret_key, value)
            logger.info(f"{info_op} Secret: *{secret_key}* in Scope: `{scope_name}`")

    def prompt_source(self):
        source = self._prompts.choice("Select the source", recon_source_choices)
        self._source = source
        return source

    def _prompt_catalog_schema(self) -> dict[str, str]:
        """
        Prompt for source, target catalog and schema names
        :return:
        """
        src_catalog_name = None
        src_schema_prompt = f"Enter `{self._source}` schema_name"

        # Prompt for `catalog_name` only if source is snowflake
        if self._source in {SourceType.SNOWFLAKE.value}:
            logger.debug(f"Prompting for `catalog_name` `database_name` for `{self._source}`")
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

        self._ensure_scope_exists(secret_scope)

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
            logger.debug(f"Filter Type: {filter_type}, Tables: {subset_tables}")
            subset_tables = [f"'{table.strip().upper()}'" for table in subset_tables.split(",")]

            include_list = subset_tables if filter_type == "include" else None
            exclude_list = subset_tables if filter_type == "exclude" else None

        # Get DataSource
        data_source = get_data_source(self._source, spark, self._ws, secret_scope)
        logger.debug(f"Listing tables for `{self._source}` using DataSource")
        # Get TableRecon config
        recon_config = data_source.list_tables(
            catalog_schema_dict.get("src_catalog"), catalog_schema_dict.get("src_schema"), include_list, exclude_list
        )

        logger.debug(f"Fetched Tables `{', '.join([table.source_name for table in recon_config.tables])}` ")

        # Update the target catalog and schema
        recon_config.target_catalog = catalog_schema_dict.get("tgt_catalog")
        recon_config.target_schema = catalog_schema_dict.get("tgt_schema")

        logger.info("Recon Config details are fetched successfully...")
        logger.debug(f"Recon Config : {recon_config}")

        return recon_config

    def _save_config_details(self, recon_config: TableRecon):
        """
        Save the config details in a file on Databricks Workspace
        """
        recon_conf_file = f"./recon_conf_{self._source}.json"

        # Create Installation object
        workspace_client = WorkspaceClient(product="remorph", product_version=__version__)
        installation = Installation(workspace_client, PRODUCT_INFO.product_name())

        logger.debug(f"Saving the config details for `{self._source}` in `{recon_conf_file}` on Databricks Workspace ")
        ws_file_url = installation.save(recon_config, filename=recon_conf_file)
        logger.debug(f"Written `{recon_conf_file}` on Databricks Workspace ")

        if self._prompts.confirm(f"Open `{recon_conf_file}` config file in the browser?"):
            webbrowser.open(ws_file_url)
        logger.info(f"Config `{recon_conf_file}` is saved at path: `{ws_file_url}` ")

    def prompt_and_save_config_details(self):
        """
        Prompt for source, target catalog and schema names. Get the table list and save the config details
        """
        # Check for Secrets Scope
        self._confirm_secret_scope()
        recon_config = self._prompt_config_details()
        logger.debug(f"recon_config_json : {json.dumps(recon_config, default=vars, indent=2, sort_keys=True)}")
        self._save_config_details(recon_config)

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
        self._ensure_scope_exists(scope_name)

        # Prompt for connection details
        connection_details = self._connection_details()
        logger.debug(f"Storing `{self._source}` connection details as Secrets in Databricks Workspace...")
        self.store_connection_secrets(scope_name, connection_details)
