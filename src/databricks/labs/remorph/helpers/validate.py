from pyspark.sql.utils import AnalysisException, ParseException

from databricks.labs.remorph.helpers.spark_connect import SparkConnectBuilder


class Validate:
    """
    The Validate class is used to validate SQL queries using a Spark session.

    Attributes:
    - config (dict): Additional configuration options for Spark.
    - connection_mode (str): The mode of the Spark session (local or remote).
    - spark (SparkSession): The Spark session used to execute and validate SQL queries.
    """

    def __init__(self, connection_mode, config=None):
        """
        Initialize the Validate class.

        Parameters:
        - connection_mode (str): The mode of the Spark session (local or remote).
        - config (dict): Additional configuration options for Spark.
        """
        self.config = config
        self.connection_mode = connection_mode
        spark_builder = SparkConnectBuilder(app_name="Validate", connection_mode=connection_mode)
        self.spark = spark_builder.build()

    # [TODO] Implement Debugger Logger
    def query(self, query: str, catalog_nm=None, schema_nm=None):
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
            if self.connection_mode.upper() == "DATABRICKS":
                if catalog_nm in (None, "transpiler_test") and schema_nm in (None, "convertor_test"):
                    spark.sql("create catalog if not exists transpiler_test")
                    spark.sql("use catalog transpiler_test")
                    spark.sql("create schema if not exists convertor_test")
                    spark.sql("use convertor_test")
                else:
                    spark.sql(f"use catalog {catalog_nm}")
                    spark.sql(f"use {schema_nm}")
            else:
                # Running in Local Mode
                pass

            # When variables is mentioned Explain fails we need way to replace them before explain is executed.
            spark.sql(query.replace("${", "`{").replace("}", "}`").replace("``", "`")).explain(True)
            return True, "Success"
        except ParseException as pe:
            # print("Syntax Exception : NOT IGNORED. Flag as syntax error :" + str(pe))
            return False, str(pe)
        except AnalysisException as aex:
            if "[TABLE_OR_VIEW_NOT_FOUND]" in str(aex):
                # print("Analysis Exception : IGNORED: " + str(aex))
                return True, str(aex)
            if "[TABLE_OR_VIEW_ALREADY_EXISTS]" in str(aex):
                # print("Analysis Exception : IGNORED: " + str(aex))
                return True, str(aex)
            elif "[UNRESOLVED_ROUTINE]" in str(aex):
                # print("Analysis Exception : NOT IGNORED: Flag as Function Missing error" + str(aex))
                return False, str(aex)
            elif "Hive support is required to CREATE Hive TABLE (AS SELECT).;" in str(aex):
                # print("Analysis Exception : IGNORED: " + str(aex))
                return True, str(aex)
            else:
                # print("Unknown Exception: " + str(aex))
                return False, str(aex)
        except Exception as e:
            # print("Other Exception : NOT IGNORED. Flagged :" + str(e))
            return False, str(e)
