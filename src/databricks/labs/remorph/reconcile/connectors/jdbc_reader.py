from typing import Any

from pyspark.sql import SparkSession

from databricks.labs.remorph.reconcile.recon_config import JdbcReaderOptions


class JDBCReaderMixin:
    _spark: SparkSession

    # TODO update the url
    def _get_jdbc_reader(self, query, jdbc_url, driver):
        driver_class = {
            "oracle": "oracle.jdbc.driver.OracleDriver",
            "snowflake": "net.snowflake.client.jdbc.SnowflakeDriver",
        }
        return (
            self._spark.read.format("jdbc")
            .option("url", jdbc_url)
            .option("driver", driver_class.get(driver, driver))
            .option("dbtable", f"({query}) tmp")
        )

    @staticmethod
    def _get_jdbc_reader_options(options: JdbcReaderOptions):
        option_dict: dict[str, Any] = {}
        if options.number_partitions:
            option_dict["numPartitions"] = options.number_partitions
        if options.partition_column:
            option_dict["partitionColumn"] = options.partition_column
        if options.lower_bound:
            option_dict["lowerBound"] = options.lower_bound
        if options.upper_bound:
            option_dict["upperBound"] = options.upper_bound
        if options.fetch_size:
            option_dict["fetchsize"] = options.fetch_size
        return option_dict
