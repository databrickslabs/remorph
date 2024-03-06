# pylint: disable=wrong-import-order,ungrouped-imports, useless-suppression)
import logging
from io import StringIO

from databricks.connect import DatabricksSession
from databricks.sdk.core import Config
from pyspark.sql.utils import AnalysisException, ParseException

from databricks.labs.remorph.config import MorphConfig

logger = logging.getLogger(__name__)


class Validate:
    """
    The Validate class is used to validate SQL queries using a Spark session.

    Attributes:
    - spark (SparkSession): The Spark session used to execute and validate SQL queries.
    """

    def __init__(self, sdk_config: Config):
        """
        Initialize the Validate class with Sparksession.
        """

        self.spark = DatabricksSession.builder.sdkConfig(sdk_config).getOrCreate()

    def use_schema(self, catalog_name, schema_name):
        try:
            self.spark.sql(f"use catalog {catalog_name}")
            self.spark.sql(f"use {schema_name}")
        except AnalysisException as aex:
            logger.error(f"Catalog or Schema not found: {aex}")
            raise aex

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
        catalog_name = config.catalog_name
        schema_name = config.schema_name
        logger.debug(f"Validation query with catalog {catalog_name} and schema {schema_name}")
        (flag, exception) = self.query(input_sql, catalog_name, schema_name)
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

    # [TODO] Implement Debugger Logger
    def query(self, query: str, catalog_name=None, schema_name=None):
        """
        Validate a given SQL query using the Spark session.

        Parameters:
        - query (str): The SQL query to be validated.
        - catalog_nm (str): The catalog name for the Spark session.
        - schema_nm (str): The schema name for the Spark session.

        Returns:
        - tuple: A tuple containing a boolean indicating whether the query is valid or not,
        and a string containing a success message or an exception message.
        """
        spark = self.spark

        try:
            # [TODO]: Explain needs to redirected to different console
            # [TODO]: Hacky way to replace variables representation
            self.use_schema(catalog_name, schema_name)
            # When variables is mentioned Explain fails we need way to replace them before explain is executed.
            spark.sql(query.replace("${", "`{").replace("}", "}`").replace("``", "`")).explain(True)
            return True, None
        except ParseException as pre:
            logger.debug(f"Syntax Exception : NOT IGNORED. Flag as syntax error: {str(pre)}")
            return False, str(pre)
        except AnalysisException as aex:
            if "[TABLE_OR_VIEW_NOT_FOUND]" in str(aex):
                logger.debug(f"Analysis Exception : IGNORED: {str(aex)}")
                return True, str(aex)
            if "[TABLE_OR_VIEW_ALREADY_EXISTS]" in str(aex):
                logger.debug(f"Analysis Exception : IGNORED: {str(aex)}")
                return True, str(aex)
            if "[UNRESOLVED_ROUTINE]" in str(aex):
                logger.debug(f"Analysis Exception : NOT IGNORED: Flag as Function Missing error {str(aex)}")
                return False, str(aex)

            if "Hive support is required to CREATE Hive TABLE (AS SELECT).;" in str(aex):
                logger.debug(f"Analysis Exception : IGNORED: {str(aex)}")
                return True, str(aex)

            logger.debug(f"Unknown Exception: {str(aex)}")
            return False, str(aex)
