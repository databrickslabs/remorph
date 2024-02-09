from io import StringIO

from databricks.labs.blueprint.entrypoint import get_logger
from databricks.sdk import WorkspaceClient

from databricks.sdk.service.sql import ServiceError

from databricks.labs.remorph.config import MorphConfig

import re 

from typing import Optional

logger = get_logger(__file__)

try: 
    from databricks.connect import DatabricksSession
except ModuleNotFoundError as e: 
    logger.error("Databricks Connect is not installed. Install the version that matches your Databricks cluster runtime version e.g., databricks-connect==14.3.0 for DBR 14.3 LTS")
    raise e 

from pyspark.sql.utils import AnalysisException, ParseException


class Validate:
    """
    The Validate class is used to validate SQL queries using a Spark session.

    Attributes:
    - spark (SparkSession): The Spark session used to execute and validate SQL queries.
    """

    def __init__(self, config: MorphConfig):
        """
        Initialize the Validate class with Sparksession.
        """

        self.client = config.sdk_client 
        self.warehouse_id = config.serverless_warehouse_id 

        self.catalog_name = config.catalog_name
        self.schema_name = config.schema_name


        ## TODO we don't need this if we are using serverless 
        if self.warehouse_id is None: 
            logger.debug("Using Databricks Connect")
            # Here we are using the MorphConfig to access the WorkSpace client, and get the SDK config 
            self.spark = DatabricksSession.builder.sdkConfig(self.client.config).getOrCreate()
        else: 
            logger.debug(f"Set serverless warehouse: {self.warehouse_id}")
            self.warehouse_id = self.warehouse_id 
    
    def _get_error_type(self, error: ServiceError) -> str: 
        error_pattern = r'\[(.*?)\]'
        match = re.search(error_pattern, error.message)

        if match: 
            return match.group(1)
        else: 
            return None 


    def validate_format_result(self, input_sql: str):
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
        catalog_name = self.catalog_name
        schema_name = self.schema_name

        is_serverless = self.warehouse_id is not None 
        
        logger.debug(f"Validation query with catalog {catalog_name} and schema {schema_name}")
        if is_serverless: 
            (flag, exception) = self.serverless_query(input_sql)
        else: 
            (flag, exception) = self.query(input_sql)
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
    def query(self, query: str):
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

        catalog_name = self.catalog_name 
        schema_name = self.schema_name

        try:
            # [TODO]: Explain needs to redirected to different console
            # [TODO]: Hacky way to replace variables representation

            # When variables is mentioned Explain fails we need way to replace them before explain is executed.
            spark.sql(query.replace("${", "`{").replace("}", "}`").replace("``", "`")).explain(True)
            return True, None
        except ParseException as pe:
            logger.debug("Syntax Exception : NOT IGNORED. Flag as syntax error :" + str(pe))
            return False, str(pe)
        except AnalysisException as aex:
            if "[TABLE_OR_VIEW_NOT_FOUND]" in str(aex):
                logger.debug("Analysis Exception : IGNORED: " + str(aex))
                return True, str(aex)
            if "[TABLE_OR_VIEW_ALREADY_EXISTS]" in str(aex):
                logger.debug("Analysis Exception : IGNORED: " + str(aex))
                return True, str(aex)
            elif "[UNRESOLVED_ROUTINE]" in str(aex):
                logger.debug("Analysis Exception : NOT IGNORED: Flag as Function Missing error" + str(aex))
                return False, str(aex)
            elif "Hive support is required to CREATE Hive TABLE (AS SELECT).;" in str(aex):
                logger.debug("Analysis Exception : IGNORED: " + str(aex))
                return True, str(aex)
            else:
                logger.debug("Unknown Exception: " + str(aex))
                return False, str(aex)
        except Exception as e:
            logger.debug("Other Exception : NOT IGNORED. Flagged :" + str(e))
            return False, str(e)
        
    def serverless_query(self, query: str): 
        client = self.client 

        catalog_name = self.catalog_name
        schema_name = self.schema_name

        ## TODO check if this is safe from SQL injection     
        explain_query = f"EXPLAIN {query}"

        try: 
            query_result = client.statement_execution.execute_statement(explain_query, catalog=catalog_name, schema=schema_name, warehouse_id=self.warehouse_id)
            error = query_result.status.error

            if error is not None: 
                error_type = self._get_error_type(error=error)
                error_message = error.message 

                if "Hive support is required to CREATE Hive TABLE (AS SELECT).;" in error_message: 
                    logger.debug(f"Analysis Exception : IGNORED: {error_message}")
                    return True, error_message 

                match error_type: 
                    case 'PARSE_SYNTAX_ERROR': 
                        logger.debug(f"Syntax Exception : NOT IGNORED. Flag as syntax error : {error_message}")
                        return False, error_message
                    case "TABLE_OR_VIEW_NOT_FOUND": 
                        logger.debug(f"Analysis Exception : IGNORED: {error_message}")
                        return True, error_message
                    case "TABLE_OR_VIEW_ALREADY_EXISTS": 
                        logger.debug(f"Analysis Exception : IGNORED: {error_message}")
                        return True, error_message 
                    case 'UNRESOLVED_ROUTINE': 
                        logger.debug(f"Analysis Exception : NOT IGNORED: Flag as Function Missing error {error_message}")
                        return False, error_message 
                    case _: 
                        logger.debug(f"Unknown Exception {error_message}")
                        return False, error_message
            else: 
                logger.info("No error message")
                return True, "No error message"
        except Exception as e: 
            logger.debug(f"Other Exception : NOT IGNORED. Flagged : {str(e)}")
                                    
