import logging

import pyspark
from pyspark.sql import DataFrame
from pyspark.sql.functions import expr

from databricks.labs.remorph.reconcile.connectors.source_adapter import SourceAdapter
from databricks.labs.remorph.reconcile.constants import (
    Constants,
    SourceDriver,
    SourceType,
)
from databricks.labs.remorph.reconcile.recon_config import (
    DatabaseConfig,
    Schema,
    Tables,
    TransformRuleMapping,
)
from pyspark.errors import PySparkException


class OracleAdapter(SourceAdapter):
    def extract_databricks_schema(self, table_conf: Tables, table_name: str) -> list[Schema]:
        pass

    def extract_schema(self, database_conf: DatabaseConfig, table_conf: Tables) -> list[Schema]:
        try:
            # get the source table name
            table_name = table_conf.source_name
            final_table_name = table_name.split(".")[-1]
            owner = table_name.split(".")[-2]
            query = f"""
            SELECT TABLE_NAME,COLUMN_NAME, DATA_TYPE, DATA_LENGTH, CHAR_LENGTH, DATA_PRECISION, DATA_SCALE, DEFAULT_LENGTH
            FROM ALL_TAB_COLUMNS
            WHERE lower(TABLE_NAME) = '{final_table_name.lower()}' and lower(owner) = '{owner.lower()}'
            """
            df = (
                self._get_oracle_reader(query)
                .load()
                .withColumn("CHAR_LENGTH", expr("cast(CHAR_LENGTH as int)"))
                .withColumn("DATA_PRECISION", expr("cast(DATA_PRECISION as int)"))
                .withColumn("DATA_SCALE", expr("cast(DATA_SCALE as int)"))
                .withColumn("DATA_LENGTH", expr("cast(DATA_LENGTH as int)"))
            )
            df.createOrReplaceTempView("oracle_schema_vw")
            processed_df = self.spark.sql(
                """
                                          select column_name, case when (data_precision is not null and data_scale <> 0) then concat(data_type,"(",data_precision,",",data_scale,")")
                                          when (data_precision is not null and data_scale == 0) then concat(data_type,"(",data_precision,")")  
                                          when data_precision is null and (lower(data_type) in ('date') or lower(data_type) like 'timestamp%') then  data_type
                                          when CHAR_LENGTH == 0 then data_type
                                          else concat(data_type,"(",CHAR_LENGTH,")")
                                          end data_type
                                          from oracle_schema_vw"""
            )

            return [Schema(field.column_name.lower(), field.data_type.lower()) for field in processed_df.collect()]
        except PySparkException as e:
            raise PySparkException(
                f"An error occurred while extracting schema for Oracle table {table_conf.source_name} in "
                f"OracleAdapter.extract_schema(): {e!s}"
            )

    def extract_data(self, table_conf: Tables, query: str) -> DataFrame:
        try:
            if table_conf.jdbc_reader_options is None:
                return self._get_oracle_reader(query).load()
            else:
                return (
                    self._get_oracle_reader(query)
                    .option("numPartitions", table_conf.jdbc_reader_options.number_partitions)
                    .option("oracle.jdbc.mapDateToTimestamp", "False")
                    .option("partitionColumn", table_conf.jdbc_reader_options.partition_column)
                    .option("lowerBound", table_conf.jdbc_reader_options.lower_bound)
                    .option("upperBound", table_conf.jdbc_reader_options.upper_bound)
                    .load()
                )
        except PySparkException as e:
            raise PySparkException(
                f"An error occurred while executing Oracle SQL query {query} in OracleAdapter.extract_data(): {e!s}"
            )

    def _get_oracle_reader(self, query: str):
        return (
            self.spark.read.format("jdbc")
            .option("url", self.get_jdbc_url)
            .option("driver", SourceDriver.ORACLE.value)
            .option("dbtable", f"({query}) tmp")
            .option("sessionInitStatement", Constants.jdbc_session_init.get(SourceType.ORACLE.value))
        )
