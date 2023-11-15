from pyspark.sql import SparkSession

from databricks.connect import DatabricksSession


class SparkConnectBuilder:
    """
    The SparkConnectBuilder class is used to build a SparkSession.

    Attributes:
    - app_name (str): The name of the Spark application.
    - config (dict): Additional configuration options for Spark.
    - spark_session (SparkSession): The Spark session to be built.
    - connection_mode (str): The mode of the Spark session (local or remote).
    """

    def __init__(self, app_name="Validate", connection_mode="LOCAL_REMOTE", config=None):
        """
        Initialize the SparkConnectBuilder class.

        Parameters:
        - app_name (str): The name of the Spark application.
        - connection_mode (str): The mode of the Spark session (local or remote).
        - config (dict): Additional configuration options for Spark.
        """
        self.app_name = app_name
        self.config = config or {}
        try:
            self.spark_session = SparkSession.getActiveSession()
        except Exception:
            self.spark_session = None
        self.connection_mode = connection_mode

    def build(self):
        """
        Build the SparkSession.

        Returns:
        - SparkSession: The instantiated SparkSession object.
        """
        if not self.spark_session:
            if self.connection_mode.upper() == "DATABRICKS":
                # [TODO]: Current Assumption default profile is used always
                spark_builder = DatabricksSession.builder.profile("DEFAULT")
            elif self.connection_mode.upper() == "LOCAL_REMOTE":
                spark_builder = SparkSession.builder.appName(self.app_name).remote("sc://localhost")
            # [Notes]: Standalone mode is not supported with Databricks Connect
            else:
                print("Not a valid Spark Connect mode, it can be 'DATABRICKS' or 'LOCAL_REMOTE'")  # noqa: T201

            for key, value in self.config.items():
                spark_builder = spark_builder.config(key, value)

            self.spark_session = spark_builder.getOrCreate()

        return self.spark_session
