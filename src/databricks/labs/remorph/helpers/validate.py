# pylint: disable=wrong-import-order,ungrouped-imports, useless-suppression)
import logging
from io import StringIO

from databricks.labs.lsql.backends import (
    DatabricksConnectBackend,
    SqlBackend,
    StatementExecutionBackend,
)
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors.base import DatabricksError

from databricks.labs.remorph.config import MorphConfig

logger = logging.getLogger(__name__)


class Validate:
    """
    The Validate class is used to validate SQL queries.
    """

    def __init__(self, ws: WorkspaceClient):
        """
        Initialize the Validate class with WorkspaceClient.
        """
        self._ws = ws

    def validate_format_result(self, config: MorphConfig, input_sql: str):
        """
        Validates the SQL query and formats the result.

        This function validates the SQL query based on the provided configuration. If the query is valid,
        it appends a semicolon to the end of the query. If the query is not valid, it formats the error message.

        Parameters:
        - config (MorphConfig): The configuration for the validation.
        - input_sql (str): The SQL query to be validated.

        Returns:
        - tuple: A tuple containing the result of the validation and the exception message (if any).
        """
        logger.debug(f"Validation query with catalog {config.catalog_name} and schema {config.schema_name}")
        sql_backend = self._get_sql_backend(config)
        (flag, exception) = self.query(sql_backend, input_sql)
        if flag:
            result = input_sql + "\n;\n"
            exception = None
        else:
            query = ""
            if "[UNRESOLVED_ROUTINE]" in exception:
                query = input_sql
            buffer = StringIO()
            buffer.write("-------------- Exception Start-------------------\n")
            buffer.write("/* \n")
            buffer.write(exception)
            buffer.write("\n */ \n")
            buffer.write(query)
            buffer.write("\n ---------------Exception End --------------------\n")

            result = buffer.getvalue()

        return result, exception

    def query(self, sql_backend: SqlBackend, query: str):
        """
        Validate a given SQL query using the Spark session.

        Parameters:
        - query (str): The SQL query to be validated.
        - sql_backend (SqlBackend): The SQL backend to be used for validation.

        Returns:
        - tuple: A tuple containing a boolean indicating whether the query is valid or not,
        and a string containing a success message or an exception message.
        """
        # When variables is mentioned Explain fails we need way to replace them before explain is executed.
        explain_query = f'EXPLAIN {query.replace("${", "`{").replace("}", "}`").replace("``", "`")}'
        try:
            sql_backend.execute(explain_query)
            return True, None
        except DatabricksError as dbe:
            err_msg = str(dbe)
            if "[PARSE_SYNTAX_ERROR]" in err_msg:
                logger.debug(f"Syntax Exception : NOT IGNORED. Flag as syntax error: {err_msg}")
                return False, err_msg
            if "[TABLE_OR_VIEW_NOT_FOUND]" in err_msg:
                logger.debug(f"Analysis Exception : IGNORED: {err_msg}")
                return True, err_msg
            if "[TABLE_OR_VIEW_ALREADY_EXISTS]" in err_msg:
                logger.debug(f"Analysis Exception : IGNORED: {err_msg}")
                return True, err_msg
            if "[UNRESOLVED_ROUTINE]" in err_msg:
                logger.debug(f"Analysis Exception : NOT IGNORED: Flag as Function Missing error {err_msg}")
                return False, err_msg

            if "Hive support is required to CREATE Hive TABLE (AS SELECT).;" in err_msg:
                logger.debug(f"Analysis Exception : IGNORED: {err_msg}")
                return True, err_msg

            logger.debug(f"Unknown Exception: {err_msg}")
            return False, err_msg

    def _get_sql_backend(self, config: MorphConfig) -> SqlBackend:
        sdk_config = self._ws.config
        warehouse_id = isinstance(sdk_config.warehouse_id, str) and sdk_config.warehouse_id
        catalog_name = config.catalog_name
        schema_name = config.schema_name
        if warehouse_id:
            sql_backend = StatementExecutionBackend(self._ws, warehouse_id, catalog=catalog_name, schema=schema_name)
        else:
            sql_backend = DatabricksConnectBackend(self._ws)
            try:
                sql_backend.execute(f"use catalog {catalog_name}")
                sql_backend.execute(f"use {schema_name}")
            except DatabricksError as dbe:
                logger.error(f"Catalog or Schema could not be selected: {dbe}")
                raise dbe
        return sql_backend
