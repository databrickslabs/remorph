from databricks.connect import DatabricksSession

from databricks.labs.blueprint.entrypoint import get_logger
from databricks.labs.blueprint.tui import Prompts

from databricks.labs.remorph.reconcile.connectors.snowflake import SnowflakeDataSource
from databricks.labs.remorph.reconcile.constants import SourceType

from databricks.sdk import WorkspaceClient

from databricks.labs.remorph.helpers.db_workspace_utils import DBWorkspaceClient

logger = get_logger(__file__)

recon_source_choices = [
    SourceType.SNOWFLAKE.value,
    SourceType.ORACLE.value,
    SourceType.DATABRICKS.value,
    SourceType.NETEZZA.value,
]


class ReconConfigPrompts:
    def __init__(self, ws: WorkspaceClient):
        self.prompts = Prompts()
        self._db_ws = DBWorkspaceClient(ws, self.prompts)

    def prompt_snowflake_connection_details(self, source: str) -> tuple[str, dict[str, str]]:
        logger.info(
            f"Please answer a couple of questions to configure `{SourceType.SNOWFLAKE.value}` Connection profile")

        sf_url = self.prompts.question("Enter Snowflake URL")
        account = self.prompts.question("Enter Account Name")
        sf_user = self.prompts.question("Enter User")
        sf_password = self.prompts.question("Enter Password")
        sf_db = self.prompts.question("Enter Database")
        sf_schema = self.prompts.question("Enter Schema")
        sf_warehouse = self.prompts.question("Enter Snowflake Warehouse")
        sf_role = self.prompts.question("Enter Role", default=" ")

        sf_conn_details = [("sfUrl", sf_url), ("account", account), ("sfUser", sf_user), ("sfPassword", sf_password),
                           ("sfDatabase", sf_db), ("sfSchema", sf_schema), ("sfWarehouse", sf_warehouse),
                           ("sfRole", sf_role)]
        sf_conn_dict = (SourceType.SNOWFLAKE.value, dict(sf_conn_details))
        return sf_conn_dict

    def prompt_oracle_connection_details(self, source: str) -> tuple[str, dict[str, str]]:
        logger.info(f"Please answer a couple of questions to configure `{SourceType.ORACLE.value}` Connection profile")
        user = self.prompts.question("Enter User")
        password = self.prompts.question("Enter Password")
        host = self.prompts.question("Enter host")
        port = self.prompts.question("Enter port")
        database = self.prompts.question("Enter database/SID")

        oracle_conn_details = [("user", user), ("password", password), ("host", host), ("port", port),
                               ("database", database)]
        oracle_conn_dict = (SourceType.ORACLE.value, dict(oracle_conn_details))
        return oracle_conn_dict

    def connection_details(self, source: str):
        logger.debug(f"Prompting for `{source}` connection details")
        match source:
            case SourceType.SNOWFLAKE.value:
                return self.prompt_snowflake_connection_details(source)
            case SourceType.ORACLE.value:
                return self.prompt_oracle_connection_details(source)
            case _:
                raise SystemExit(f"Source {source} is not yet configured...")

    def prompt_connection_details(self, source: str):
        # prompt for connection_details only if source is other than Databricks
        if source == SourceType.DATABRICKS.value:
            logger.info("*Databricks* as a source is supported only for **Hive MetaStore setup**")
            return

        scope_name = self.prompts.question("Enter Scope name")
        self._db_ws.get_or_create_scope(scope_name)

        connection_details = self.connection_details(source)
        logger.debug(f"Storing `{source}` connection details as Secrets in Databricks Workspace...")
        self._db_ws.store_connection_secrets(scope_name, connection_details)

    def prompt_catalog_schema(self, source: str) -> tuple[str, str]:
        """Prompt for `catalog_name` only if source is snowflake"""

        prompt_for_catalog = source in {SourceType.SNOWFLAKE.value}
        catalog_name = self.prompts.question("Enter catalog_name") if prompt_for_catalog else ""
        schema_name = self.prompts.question("Enter schema_name")

        return catalog_name, schema_name

    def prompt_config_details(self, source: str) -> tuple[str, str]:
        # Prompt for secret scope
        secret_scope = self.prompts.question(f"Enter `{source}` Secret Scope name")
        if not self._db_ws.scope_exists(secret_scope):
            msg = ("Error: Secret Scope not found in Databricks Workspace."
                   "\nUse `remorph setup-recon-secrets` to setup Scope and Secrets")
            raise SystemExit(msg)

        # Prompt for catalog and schema
        catalog, schema = self.prompt_catalog_schema(source)
        spark = DatabricksSession.builder.getOrCreate()

        only_subset = self.prompts.confirm(f"Do you want to include/exclude a set of tables?")
        if only_subset:
            # Prompt for filter
            filter_types = ["include", "exclude"]
            filter_type = self.prompts.choice("Select the filter type", filter_types)
            subset_tables = self.prompts.question(f"Enter the tables(separated by comma) to `{filter_type}`")

            # crawler, source adapter
            sf_datasource = SnowflakeDataSource(source, spark, self._db_ws.ws, secret_scope)
            # schema = sf_datasource.get_schema_query(catalog, schema, "supplier")
            print(catalog, schema, source)
