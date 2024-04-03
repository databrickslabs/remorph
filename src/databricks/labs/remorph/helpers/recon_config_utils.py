from databricks.labs.blueprint.entrypoint import get_logger
from databricks.labs.blueprint.tui import Prompts

from databricks.labs.remorph.reconcile.constants import SourceType

logger = get_logger(__file__)


class ReconConfigPrompts:
    def __init__(self):
        self.prompts = Prompts()

    def prompt_catalog_schema(self, source: str) -> tuple[str, str]:
        """Prompt for `catalog_name` only if source is snowflake"""
        if source == SourceType.DATABRICKS.value:
            logger.info("Databricks source is supported only for Hive MetaStore setup")
        prompt_for_catalog = source in {SourceType.SNOWFLAKE.value}
        catalog_name = self.prompts.question("Enter catalog_name") if prompt_for_catalog else ""
        schema_name = self.prompts.question("Enter schema_name")

        return catalog_name, schema_name

    def prompt_snowflake_connection_details(self, source: str) -> tuple[str, str]:
        """
        [snowflake]
        sfUrl = <url>
        account = <acount_name>
        sfUser = <user>
        sfPassword = <password>
        sfDatabase = <database>
        sfSchema = <schema>
        sfWarehouse = <warehouse_name>
        sfRole = <role_name>
        """

    def prompt_oracle_connection_details(self, source: str) -> tuple[str, str]:
        """
        [oracle]
        user = <user>
        password = <password>
        host = <host>
        port = <port>
        database = <database/SID>
        """

    def prompt_connection_details(self, source: str) -> tuple[str, str]:
        # prompt for connection_details only if source is other than Databricks
        prompt_for_connection_details = source != "databricks"
        catalog_name = self.prompts.question("Enter catalog_name") if prompt_for_connection_details else ""
        schema_name = self.prompts.question("Enter schema_name")

        return catalog_name, schema_name
