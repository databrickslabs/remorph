from io import StringIO

from databricks.connect import DatabricksSession
from databricks.labs.blueprint.entrypoint import get_logger
from databricks.sdk import WorkspaceClient
from pyspark.sql.utils import AnalysisException, ParseException

from databricks.sdk.service.sql import ServiceError

from databricks.labs.remorph.config import MorphConfig

import re 

from typing import Optional

logger = get_logger(__file__)


class Validate:
    """
    The Validate class is used to validate SQL queries using a Spark session.

    Attributes:
    - spark (SparkSession): The Spark session used to execute and validate SQL queries.
    """

    def __init__(self, w: WorkspaceClient, warehouse_id: Optional[str] = None):
        """
        Initialize the Validate class with Sparksession.
        """

        self.w = w 

        ## TODO we don't need this if we are using serverless 
        if warehouse_id is not None: 
            self.spark = DatabricksSession.builder.sdkConfig(w.config).getOrCreate()
        else: 
            self.warehouse_id = warehouse_id 
    
    def _create_test_catalog(self, catalog_name=None, schema_name=None): 
        w = self.w 
        if catalog_name in (None, 'transpiler_test') and schema_name in (None, 'convertor_test'): 
            logger.debug("Creating catalog and schema for Remorph")
            try: 
                w.catalogs.create(name='transpiler_test', comment='Catalog created by Remorph for query validation')

            ## TODO there has to be a smarter way to test if a Catalog exists
            ## my thought is if we `list` the catalogs that is a big operation for
            ## large worksapces 
            except: 
                logger.info("Catalog already exists")
            try: 
                w.schema.create(name='convertor_test', catalog_name='transpiler_teste', comment='Schema created by Remorph for query validation')
            except: 
                logger.info("Schema already exists") 
    
    def _get_error_type(self, error: ServiceError) -> str: 
        error_pattern = r'\[(.*?)\]'
        match = re.search(error_pattern, error.message)

        if match: 
            return match.group(1)
        else: 
            return None 


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

        is_serverless = config.serverless_warehouse_id is not None 
        
        logger.debug(f"Validation query with catalog {catalog_name} and schema {schema_name}")
        if is_serverless: 
            (flag, exception) = self.serverless_query(input_sql, catalog_name, schema_name)
        else: 
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
            if catalog_name in (None, "transpiler_test") and schema_name in (None, "convertor_test"):
                spark.sql("create catalog if not exists transpiler_test")
                spark.sql("use catalog transpiler_test")
                spark.sql("create schema if not exists convertor_test")
                spark.sql("use convertor_test")
            else:
                spark.sql(f"use catalog {catalog_name}")
                spark.sql(f"use {schema_name}")

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
        
    def serverless_query(self, query: str, catalog_name=None, schema_name=None): 
        w = self.w 

        _create_test_catalog(catalog_name=catalog_name, schema_name=schema_name)

        ## TODO check if this is safe from SQL injection     
        explain_query = f"EXPLAIN {query}"

        logger.debug("running sql query")
        try: 
            query_result = w.statement_execution.execute_statement(explain_query, catalog=catalog_name, schema=schema_name)
            error = query_result.status.error

            if error is not None: 
                error_type = _get_error_type(error=error)
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
        except Exception as e: 
            logger.debug(f"Other Exception : NOT IGNORED. Flagged : {str(e)}")
                                    
