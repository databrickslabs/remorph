from pyspark.sql import SparkSession

from databricks.labs.remorph.reconcile.recon_config import JdbcReaderOptions


class JDBCReaderMixin:
    _spark: SparkSession

    # TODO update the url
    def _get_jdbc_reader(self, query, jdbc_url, driver, prepare_query=""):
        driver_class = {
            "oracle": "oracle.jdbc.driver.OracleDriver",
            "snowflake": "net.snowflake.client.jdbc.SnowflakeDriver",
            "sqlserver": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
        }
        return (
            self._spark.read.format("jdbc")
            .option("url", jdbc_url)
            .option("driver", driver_class.get(driver, driver))
            .option('prepareQuery', prepare_query)
            .option("dbtable", f"({query}) tmp")
        )

    @staticmethod
    def _get_jdbc_reader_options(options: JdbcReaderOptions):
        return {
            "numPartitions": options.number_partitions,
            "partitionColumn": options.partition_column,
            "lowerBound": options.lower_bound,
            "upperBound": options.upper_bound,
            "fetchsize": options.fetch_size,
        }
