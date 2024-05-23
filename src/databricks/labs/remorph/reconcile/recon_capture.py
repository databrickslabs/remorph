import logging
from datetime import datetime

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, collect_list, create_map, lit
from sqlglot import Dialect

from databricks.labs.remorph.config import DatabaseConfig, Table
from databricks.labs.remorph.reconcile.exception import WriteToTableException
from databricks.labs.remorph.reconcile.recon_config import (
    DataReconcileOutput,
    ReconcileProcessDuration,
    SchemaReconcileOutput,
)
from databricks.sdk import WorkspaceClient

logger = logging.getLogger(__name__)


def _write_df_to_delta(df: DataFrame, table_name: str, mode="append"):
    try:
        df.write.mode(mode).saveAsTable(table_name)
        logger.info(f"Data written to {table_name}")
    except Exception as e:
        message = f"Error writing data to {table_name}: {e}"
        logger.error(message)
        raise WriteToTableException(message) from e


class ReconCapture:
    _REMORPH_CATALOG = "remorph"
    _RECONCILE_SCHEMA = "reconcile"
    _DB_PREFIX = f"{_REMORPH_CATALOG}.{_RECONCILE_SCHEMA}"
    _RECON_TABLE_NAME = "main"
    _RECON_METRICS_TABLE_NAME = "metrics"
    _RECON_DETAILS_TABLE_NAME = "details"

    def __init__(
        self,
        database_config: DatabaseConfig,
        recon_id: str,
        report_type: str,
        source_dialect: Dialect,
        ws: WorkspaceClient,
        spark: SparkSession,
    ):
        self.database_config = database_config
        self.recon_id = recon_id
        self.report_type = report_type
        self.source_dialect = source_dialect
        self.ws = ws
        self.spark = spark

    def _generate_recon_main_id(
        self,
        table_conf: Table,
    ) -> int:
        full_source_table = (
            f"{self.database_config.source_schema}.{table_conf.source_name}"
            if self.database_config.source_catalog is None
            else f"{self.database_config.source_catalog}.{self.database_config.source_schema}.{table_conf.source_name}"
        )
        full_target_table = (
            f"{self.database_config.target_catalog}.{self.database_config.target_schema}.{table_conf.target_name}"
        )
        return hash(f"{self.recon_id}{full_source_table}{full_target_table}")

    def _insert_into_main_table(
        self,
        recon_table_id: int,
        table_conf: Table,
        recon_process_duration: ReconcileProcessDuration,
    ) -> None:
        df = self.spark.sql(
            f"""
                select {recon_table_id} as recon_table_id,
                '{self.recon_id}' as recon_id,
                case 
                    when '{str(self.source_dialect)}' like '%Snow%' then 'Snowflake' 
                    when '{str(self.source_dialect)}' like '%Oracle%' then 'Oracle'
                    when '{str(self.source_dialect)}' like '%Databricks%' then 'Databricks'
                    else '{str(self.source_dialect)}' 
                end as source_type,
                named_struct(
                    'catalog', '{self.database_config.source_catalog}', 
                    'schema', '{self.database_config.source_schema}', 
                    'table_name', '{table_conf.source_name}'
                ) as source_table,
                named_struct(
                    'catalog', '{self.database_config.target_catalog}', 
                    'schema', '{self.database_config.target_schema}', 
                    'table_name', '{table_conf.target_name}'
                ) as target_table,
                '{self.report_type}' as report_type,
                cast('{recon_process_duration.start_ts}' as timestamp) as start_ts,
                cast('{recon_process_duration.end_ts}' as timestamp) as end_ts
            """
        )
        _write_df_to_delta(df, f"{self._DB_PREFIX}.{self._RECON_TABLE_NAME}")

    def _insert_into_metrics_table(
        self,
        recon_table_id: int,
        data_reconcile_output: DataReconcileOutput,
        schema_reconcile_output: SchemaReconcileOutput,
    ) -> None:
        status = False
        if data_reconcile_output.exception in {None, ''} and schema_reconcile_output.exception in {None, ''}:
            status = not (
                data_reconcile_output.mismatch_count > 0
                or data_reconcile_output.missing_in_src_count > 0
                or data_reconcile_output.missing_in_tgt_count > 0
                or not schema_reconcile_output.is_valid
                or data_reconcile_output.threshold_output.threshold_mismatch_count > 0
            )

        exception_msg = ""
        if schema_reconcile_output.exception is not None:
            exception_msg = schema_reconcile_output.exception
        if data_reconcile_output.exception is not None:
            exception_msg = data_reconcile_output.exception

        insertion_time = str(datetime.now())

        df = self.spark.sql(
            f"""
                select {recon_table_id} as recon_table_id,
                named_struct(
                    'row_comparison', named_struct(
                        'missing_in_source', {data_reconcile_output.missing_in_src_count},
                        'missing_in_target', {data_reconcile_output.missing_in_tgt_count}
                    ),
                    'column_comparison', named_struct(
                        'absolute_mismatch', {data_reconcile_output.mismatch_count},
                        'threshold_mismatch', {data_reconcile_output.threshold_output.threshold_mismatch_count},
                        'mismatch_columns', '{",".join(data_reconcile_output.mismatch.mismatch_columns)}'
                    ),
                    'schema_comparison', {schema_reconcile_output.is_valid}
                ) as recon_metrics,
                named_struct(
                    'status', {status}, 
                    'run_by_user', '{self.ws.current_user.me().user_name}', 
                    'exception_message', "{exception_msg}"
                ) as run_metrics,
                cast('{insertion_time}' as timestamp) as inserted_ts
            """
        )
        _write_df_to_delta(df, f"{self._DB_PREFIX}.{self._RECON_METRICS_TABLE_NAME}")

    @classmethod
    def _create_map_column(
        cls,
        recon_table_id: int,
        df: DataFrame,
        recon_type: str,
        status: bool,
    ) -> DataFrame:
        columns = df.columns
        # Create a list of column names and their corresponding column values
        map_args = []
        for column in columns:
            map_args.extend([lit(column).alias(column + "_key"), col(column).cast("string").alias(column + "_value")])
        # Create a new DataFrame with a map column
        df = df.select(create_map(*map_args).alias("data"))
        df = (
            df.withColumn("recon_table_id", lit(recon_table_id))
            .withColumn("recon_type", lit(recon_type))
            .withColumn("status", lit(status))
            .withColumn("inserted_ts", lit(datetime.now()))
        )
        return (
            df.groupBy("recon_table_id", "recon_type", "status", "inserted_ts")
            .agg(collect_list("data").alias("data"))
            .selectExpr("recon_table_id", "recon_type", "status", "data", "inserted_ts")
        )

    def _create_map_column_and_insert(
        self,
        recon_table_id: int,
        df: DataFrame,
        recon_type: str,
        status: bool,
    ) -> None:
        df = self._create_map_column(recon_table_id, df, recon_type, status)
        _write_df_to_delta(df, f"{self._DB_PREFIX}.{self._RECON_DETAILS_TABLE_NAME}")

    def _insert_into_details_table(
        self,
        recon_table_id: int,
        reconcile_output: DataReconcileOutput,
        schema_output: SchemaReconcileOutput,
    ):
        if reconcile_output.mismatch_count > 0:
            self._create_map_column_and_insert(
                recon_table_id,
                reconcile_output.mismatch.mismatch_df,
                "mismatch",
                False,
            )

        if reconcile_output.missing_in_src_count > 0:
            self._create_map_column_and_insert(
                recon_table_id,
                reconcile_output.missing_in_src,
                "missing_in_source",
                False,
            )

        if reconcile_output.missing_in_tgt_count > 0:
            self._create_map_column_and_insert(
                recon_table_id,
                reconcile_output.missing_in_tgt,
                "missing_in_target",
                False,
            )

        if reconcile_output.threshold_output.threshold_mismatch_count > 0:
            self._create_map_column_and_insert(
                recon_table_id,
                reconcile_output.threshold_output.threshold_df,
                "threshold_mismatch",
                False,
            )

        if schema_output.compare_df is not None:
            self._create_map_column_and_insert(
                recon_table_id, schema_output.compare_df, "schema", schema_output.is_valid
            )

    def start(
        self,
        data_reconcile_output: DataReconcileOutput,
        schema_reconcile_output: SchemaReconcileOutput,
        table_conf: Table,
        recon_process_duration: ReconcileProcessDuration,
    ) -> None:
        recon_table_id = self._generate_recon_main_id(table_conf)
        self._insert_into_main_table(recon_table_id, table_conf, recon_process_duration)
        self._insert_into_metrics_table(recon_table_id, data_reconcile_output, schema_reconcile_output)
        self._insert_into_details_table(recon_table_id, data_reconcile_output, schema_reconcile_output)
