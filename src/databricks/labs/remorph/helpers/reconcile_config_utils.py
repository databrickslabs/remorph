import json
import logging
import webbrowser

from databricks.connect import DatabricksSession
from databricks.labs.blueprint.installation import Installation, SerdeError
from databricks.labs.blueprint.tui import Prompts
from databricks.labs.remorph.config import TableRecon, ReconcileConfig, get_dialect, ReconcileTablesConfig
from databricks.labs.remorph.reconcile.connectors.source_adapter import create_adapter
from databricks.labs.remorph.reconcile.constants import SourceType
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors.platform import ResourceDoesNotExist, NotFound, PermissionDenied

logger = logging.getLogger(__name__)

README_RECON_CONFIG_NOTEBOOK = """# Databricks notebook source
# MAGIC %md
# MAGIC # Recon Config setup instructions (see [README](readme_link))
# MAGIC
# MAGIC Production runs are supposed to be triggered through the following jobs: job_links
# MAGIC
# MAGIC **This notebook is overwritten with each `remorph` generate-recon-config.**

# COMMAND ----------

# MAGIC %pip install remorph_VERSION-py3-none-any.whl
dbutils.library.restartPython()

# COMMAND ----------

from databricks.labs.remorph.config import get_dialect
from databricks.labs.remorph.reconcile.recon_config import ColumnMapping, Schema, Table
from databricks.labs.remorph.reconcile.schema_compare import SchemaCompare

    sparkSession = SparkSession.builder.getOrCreate() 
    table_conf = Table(
        source_name="src_table",
        target_name="tgt_table",
        column_mapping=[
            ColumnMapping(source_name="col_1", target_name="col1"),
            ColumnMapping(source_name="col_2", target_name="col2"),
        ],
    )
snowflake_dialect = get_dialect("snowflake")

output = SchemaCompare(sparkSession).compare(
    source_schema,
    target_schema,
    snowflake_dialect,
    table_conf,
)
compared_df = output.compare_df
"""


class ReconcileConfigUtils:
    def __init__(self, ws: WorkspaceClient, installation: Installation, prompts: Prompts = Prompts()):
        self._source = None
        self._prompts = prompts
        self._ws = ws
        self._installation = installation
        self._reconcile_config: ReconcileConfig | None = None

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

    def _ensure_scope_exists(self, scope_name: str | None = None):
        """
        Get or Create a new Scope in Databricks Workspace
        """
        scope_name = self._reconcile_config.secret_scope if self._reconcile_config else scope_name
        assert scope_name, "Secret Scope is not set"

        scope_exists = self._scope_exists(scope_name)
        if not scope_exists:
            allow_scope_creation = self._prompts.confirm("Do you want to create a new one?")
            if not allow_scope_creation:
                msg = f" `{scope_name}` Scope is needed to store Secrets in Databricks Workspace"
                raise SystemExit(msg)

            try:
                logger.debug(f" Creating a new Scope: `{scope_name}`")
                self._ws.secrets.create_scope(scope_name)
            except RuntimeError as ex:
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
        except RuntimeError as ex:
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
        data_source = self._prompts.choice(
            "Select the Data Source:",
            [SourceType.DATABRICKS.value, SourceType.SNOWFLAKE.value, SourceType.ORACLE.value],
        )
        self._source = data_source
        return data_source

    def _confirm_secret_scope(self):
        if not self._prompts.confirm(
            f"Did you setup the secrets for the `{self._reconcile_config.data_source.capitalize()}` connection "
            f"in `{self._reconcile_config.secret_scope}` Scope?"
        ):
            raise ValueError(
                f"Error: Secrets are needed for `{self._reconcile_config.data_source.capitalize()}` reconciliation."
                f"\nUse `remorph configure-secrets` to setup Scope and Secrets."
            )

    def _create_recon_config_readme(self):
        content = README_RECON_CONFIG_NOTEBOOK.encode("utf8")
        self._installation.upload('README_RECON_CONFIG.py', content)
        return self._installation.workspace_link('README_RECON_CONFIG')

    def _save_recon_config_details(self, details: tuple[TableRecon, str]):
        """
        Save the config details in a file on Databricks Workspace
        """
        assert self._reconcile_config, "Reconcile Config is not set"

        recon_config, file_name = details
        recon_config_json = json.dumps(recon_config, default=vars, indent=2, sort_keys=True)
        logger.debug(f"recon_config_json : {recon_config_json}")

        logger.debug(
            f"Saving the reconcile_config details for `{self._reconcile_config.data_source}` "
            f"in `{file_name}` on Databricks Workspace "
        )
        self._installation.upload(filename=file_name, raw=recon_config_json.encode("utf-8"))
        ws_file_url = self._installation.workspace_link(file_name)
        logger.debug(f"Written `{file_name}` on Databricks Workspace ")

        if self._prompts.confirm(f"Open `{file_name}` config file in the browser?"):
            webbrowser.open(ws_file_url)
        logger.info(f"Config `{file_name}` is saved at path: `{ws_file_url}` ")

        reconcile_readme_url = self._create_recon_config_readme()
        if self._prompts.confirm("Open `README_RECON_CONFIG` setup instructions in your browser?"):
            webbrowser.open(reconcile_readme_url)
        logger.info(
            f"Recon Config generated successfully! Please refer to the {reconcile_readme_url} for the next steps."
        )

        return ws_file_url

    def _confirm_or_prompt_for_tables_subset(self) -> tuple[bool, ReconcileTablesConfig]:
        tables_updated = False
        assert self._reconcile_config, "Reconcile Config is not set"

        if self._reconcile_config.tables:
            tables_config = self._reconcile_config.tables
            filter_type, subset_tables_list = tables_config.filter_type, tables_config.tables_list

            proceed_run_prompt = "Would you like to run reconciliation for `all` tables?"
            if filter_type != "all":
                proceed_run_prompt = (
                    f"Would you like to run reconciliation `{filter_type[:-1]}ing` "
                    f" {','.join(subset_tables_list)} tables? "
                )

            proceed_run = self._prompts.confirm(proceed_run_prompt)
            if proceed_run:
                return tables_updated, tables_config

        filter_type = self._prompts.choice(
            "Would you like to run reconciliation on `all` tables OR on a `subset of tables`? "
            "Please choose the `subset type` or select `all`:",
            ["include", "exclude", "all"],
        )

        tables_config = ReconcileTablesConfig(filter_type="all", tables_list=["*"])

        if filter_type != "all":
            subset_tables = self._prompts.question(f"Comma-separated list of tables to `{filter_type}`")
            logger.debug(f"Filter Type: `{filter_type}`, Tables: `{subset_tables}`")
            subset_tables_list = [table.strip().upper() for table in subset_tables.split(",")]
            tables_config = ReconcileTablesConfig(filter_type=filter_type, tables_list=subset_tables_list)

        return True, tables_config

    def _save_reconcile_config(self, config: ReconcileConfig):
        logger.info("Saving the ** reconcile ** configuration in Databricks Workspace")
        self._installation.save(config)

    def _generate_table_recon(self) -> tuple[TableRecon, str]:

        assert self._reconcile_config, "Reconcile Config is not set"
        source = None
        if self._reconcile_config.data_source:
            source = self._reconcile_config.data_source

        assert source, "Data Source is not set in `reconcile_config`"

        include_list: list[str] | None = None
        exclude_list: list[str] | None = None
        spark = DatabricksSession.builder.getOrCreate()

        tables_updated, tables = self._confirm_or_prompt_for_tables_subset()
        filter_type, subset_tables_raw = tables.filter_type, tables.tables_list
        if tables_updated:
            self._reconcile_config.tables = ReconcileTablesConfig(filter_type, subset_tables_raw)
            # Save Reconcile Config details on Databricks workspace with `tables` field
            self._save_reconcile_config(self._reconcile_config)

        if filter_type != "all":
            subset_tables = [f"'{table}'" for table in subset_tables_raw]
            include_list = subset_tables if filter_type == "include" else None
            exclude_list = subset_tables if filter_type == "exclude" else None

        # Get DataSource
        data_source = create_adapter(get_dialect(source), spark, self._ws, self._reconcile_config.secret_scope)
        logger.info(f"Listing tables for `{source.capitalize()}` using DataSource")

        # Get TableRecon config
        recon_config = data_source.list_tables(
            self._reconcile_config.database_config.source_catalog,
            self._reconcile_config.database_config.source_schema,
            include_list,
            exclude_list,
        )

        logger.debug(f"Fetched Tables `{', '.join([table.source_name for table in recon_config.tables])}` ")

        # Update the target catalog and schema
        recon_config.target_catalog = self._reconcile_config.database_config.target_catalog
        recon_config.target_schema = self._reconcile_config.database_config.target_schema

        logger.info("Recon Config details are fetched successfully...")
        logger.debug(f"Recon Config : {recon_config}")

        file_name = (
            f"recon_config_{source}" f"_{self._reconcile_config.database_config.source_catalog}" f"_{filter_type}.json"
        )

        return recon_config, file_name

    def generate_recon_config(self):
        """
        Prompt for source, target catalog and schema names. Get the table list and save the config details
        """

        reconcile_config = None
        try:
            reconcile_config = self._installation.load(ReconcileConfig)
        except NotFound as err:
            logger.debug(f"Cannot find previous `reconcile` installation: {err}")
        except (PermissionDenied, SerdeError, ValueError, AttributeError) as ex:
            logger.warning(
                f"Existing installation at {self._installation.install_folder()} is corrupted. Skipping... \n"
                f"Exception: {ex}"
            )

        reconfigure_msg = "Please use `remorph install` to re-configure ** reconcile ** module"
        # Reconfigure `reconcile` module:
        # * when there is no `reconcile.yml` config on Databricks workspace OR
        # * when there is `reconcile.yml` and user wants to overwrite it
        if not reconcile_config:
            logger.info(f"`reconcile_config` not found on Databricks Workspace.\n{reconfigure_msg}")
            return
        if self._prompts.confirm(
            f"Would you like to overwrite workspace `reconcile_config` values:\n" f" {reconcile_config.__dict__}?"
        ):
            logger.info(reconfigure_msg)
            return

        self._reconcile_config = reconcile_config
        # Check for Scope and ensure Secrets are set up
        self._ensure_scope_exists()
        self._confirm_secret_scope()

        self._save_recon_config_details(self._generate_table_recon())

    def _prompt_snowflake_connection_details(self) -> tuple[str, dict[str, str]]:
        """
        Prompt for Snowflake connection details
        :return: tuple[str, dict[str, str]]
        """
        logger.info(f"Please answer a few questions to configure `{SourceType.SNOWFLAKE.value}` Connection profile")

        sf_url = self._prompts.question("Enter Snowflake URL")
        account = self._prompts.question("Enter Account Name")
        sf_user = self._prompts.question("Enter User")
        sf_password = self._prompts.question("Enter Password")
        sf_db = self._prompts.question("Enter Catalog")
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
        logger.info(f"Please answer a few questions to configure `{SourceType.ORACLE.value}` Connection profile")
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
