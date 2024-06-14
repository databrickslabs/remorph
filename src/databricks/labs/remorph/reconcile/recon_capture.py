import logging
from datetime import datetime

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, collect_list, create_map, lit
from pyspark.sql.types import StringType, StructField, StructType
from pyspark.errors import PySparkException
from sqlglot import Dialect

from databricks.labs.remorph.config import DatabaseConfig, Table, get_key_from_dialect, ReconcileMetadataConfig
from databricks.labs.remorph.reconcile.exception import (
    WriteToTableException,
    ReadAndWriteWithVolumeException,
    CleanFromVolumeException,
)
from databricks.labs.remorph.reconcile.recon_config import (
    DataReconcileOutput,
    ReconcileOutput,
    ReconcileProcessDuration,
    ReconcileTableOutput,
    SchemaReconcileOutput,
    StatusOutput,
)
from databricks.sdk import WorkspaceClient

logger = logging.getLogger(__name__)

_RECON_TABLE_NAME = "main"
_RECON_METRICS_TABLE_NAME = "metrics"
_RECON_DETAILS_TABLE_NAME = "details"
_SAMPLE_ROWS = 50


class ReconIntermediatePersist:

    def __init__(self, spark: SparkSession, path: str):
        self.spark = spark
        self.path = path

    def _write_unmatched_df_to_volumes(
        self,
        unmatched_df: DataFrame,
    ) -> None:
        unmatched_df.write.format("parquet").mode("overwrite").save(self.path)

    def _read_unmatched_df_from_volumes(self) -> DataFrame:
        return self.spark.read.format("parquet").load(self.path)

    def clean_unmatched_df_from_volume(self):
        try:
            # TODO: for now we are overwriting the intermediate cache path. We should delete the volume in future
            # workspace_client.dbfs.get_status(path)
            # workspace_client.dbfs.delete(path, recursive=True)
            empty_df = self.spark.createDataFrame([], schema=StructType([StructField("empty", StringType(), True)]))
            empty_df.write.format("parquet").mode("overwrite").save(self.path)
            logger.warning(f"Unmatched DF cleaned up from {self.path} successfully.")
        except PySparkException as e:
            message = f"Error cleaning up unmatched DF from {self.path} volumes --> {e}"
            logger.error(message)
            raise CleanFromVolumeException(message) from e

    def write_and_read_unmatched_df_with_volumes(
        self,
        unmatched_df: DataFrame,
    ) -> DataFrame:
        try:
            self._write_unmatched_df_to_volumes(unmatched_df)
            return self._read_unmatched_df_from_volumes()
        except PySparkException as e:
            message = f"Exception in reading or writing unmatched DF with volumes {self.path} --> {e}"
            logger.error(message)
            raise ReadAndWriteWithVolumeException(message) from e


def _write_df_to_delta(df: DataFrame, table_name: str, mode="append"):
    try:
        df.write.mode(mode).saveAsTable(table_name)
        logger.info(f"Data written to {table_name} successfully.")
    except Exception as e:
        message = f"Error writing data to {table_name}: {e}"
        logger.error(message)
        raise WriteToTableException(message) from e


def generate_final_reconcile_output(
    recon_id: str,
    spark: SparkSession,
    metadata_config: ReconcileMetadataConfig = ReconcileMetadataConfig(),
    local_test_run: bool = False,
) -> ReconcileOutput:
    _db_prefix = "default" if local_test_run else f"{metadata_config.catalog}.{metadata_config.schema}"
    recon_df = spark.sql(
        f"""
    SELECT 
    CASE 
        WHEN COALESCE(MAIN.SOURCE_TABLE.CATALOG, '') <> '' THEN CONCAT(MAIN.SOURCE_TABLE.CATALOG, '.', MAIN.SOURCE_TABLE.SCHEMA, '.', MAIN.SOURCE_TABLE.TABLE_NAME) 
        ELSE CONCAT(MAIN.SOURCE_TABLE.SCHEMA, '.', MAIN.SOURCE_TABLE.TABLE_NAME) 
    END AS SOURCE_TABLE, 
    CONCAT(MAIN.TARGET_TABLE.CATALOG, '.', MAIN.TARGET_TABLE.SCHEMA, '.', MAIN.TARGET_TABLE.TABLE_NAME) AS TARGET_TABLE, 
    CASE WHEN lower(MAIN.report_type) in ('all', 'row', 'data') THEN
    CASE 
        WHEN METRICS.recon_metrics.row_comparison.missing_in_source = 0 AND METRICS.recon_metrics.row_comparison.missing_in_target = 0 THEN TRUE 
        ELSE FALSE 
    END 
    ELSE NULL END AS ROW, 
    CASE WHEN lower(MAIN.report_type) in ('all', 'data') THEN
    CASE 
        WHEN METRICS.recon_metrics.column_comparison.absolute_mismatch = 0 AND METRICS.recon_metrics.column_comparison.threshold_mismatch = 0 AND METRICS.recon_metrics.column_comparison.mismatch_columns = '' THEN TRUE 
        ELSE FALSE 
    END 
    ELSE NULL END AS COLUMN, 
    CASE WHEN lower(MAIN.report_type) in ('all', 'schema') THEN
    CASE 
        WHEN METRICS.recon_metrics.schema_comparison = true THEN TRUE 
        ELSE FALSE 
    END
    ELSE NULL END AS SCHEMA,
    METRICS.run_metrics.exception_message AS EXCEPTION_MESSAGE 
    FROM 
        {_db_prefix}.{_RECON_TABLE_NAME} MAIN 
    INNER JOIN 
        {_db_prefix}.{_RECON_METRICS_TABLE_NAME} METRICS 
    ON 
        (MAIN.recon_table_id = METRICS.recon_table_id) 
    WHERE 
        MAIN.recon_id = '{recon_id}' 
    """
    )
    table_output = []
    for row in recon_df.collect():
        if row.EXCEPTION_MESSAGE is not None and row.EXCEPTION_MESSAGE != "":
            table_output.append(
                ReconcileTableOutput(
                    target_table_name=row.TARGET_TABLE,
                    source_table_name=row.SOURCE_TABLE,
                    status=StatusOutput(),
                    exception_message=row.EXCEPTION_MESSAGE,
                )
            )
        else:
            table_output.append(
                ReconcileTableOutput(
                    target_table_name=row.TARGET_TABLE,
                    source_table_name=row.SOURCE_TABLE,
                    status=StatusOutput(row=row.ROW, column=row.COLUMN, schema=row.SCHEMA),
                    exception_message=row.EXCEPTION_MESSAGE,
                )
            )
    final_reconcile_output = ReconcileOutput(recon_id=recon_id, results=table_output)
    logger.info(f"Final reconcile output: {final_reconcile_output}")
    return final_reconcile_output


class ReconCapture:

    def __init__(
        self,
        database_config: DatabaseConfig,
        recon_id: str,
        report_type: str,
        source_dialect: Dialect,
        ws: WorkspaceClient,
        spark: SparkSession,
        metadata_config: ReconcileMetadataConfig = ReconcileMetadataConfig(),
        local_test_run: bool = False,
    ):
        self.database_config = database_config
        self.recon_id = recon_id
        self.report_type = report_type
        self.source_dialect = source_dialect
        self.ws = ws
        self.spark = spark
        self._db_prefix = "default" if local_test_run else f"{metadata_config.catalog}.{metadata_config.schema}"

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
        source_dialect_key = get_key_from_dialect(self.source_dialect)
        df = self.spark.sql(
            f"""
                select {recon_table_id} as recon_table_id,
                '{self.recon_id}' as recon_id,
                case 
                    when '{source_dialect_key}' = 'databricks' then 'Databricks'
                    when '{source_dialect_key}' = 'snowflake' then 'Snowflake'
                    when '{source_dialect_key}' = 'oracle' then 'Oracle'
                    else '{source_dialect_key}'
                end as source_type,
                named_struct(
                    'catalog', case when '{self.database_config.source_catalog}' = 'None' then null else '{self.database_config.source_catalog}' end, 
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
        _write_df_to_delta(df, f"{self._db_prefix}.{_RECON_TABLE_NAME}")

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
            exception_msg = schema_reconcile_output.exception.replace("'", '').replace('"', '')
        if data_reconcile_output.exception is not None:
            exception_msg = data_reconcile_output.exception.replace("'", '').replace('"', '')

        insertion_time = str(datetime.now())
        mismatch_columns = []
        if data_reconcile_output.mismatch and data_reconcile_output.mismatch.mismatch_columns:
            mismatch_columns = data_reconcile_output.mismatch.mismatch_columns

        df = self.spark.sql(
            f"""
                select {recon_table_id} as recon_table_id,
                named_struct(
                    'row_comparison', case when '{self.report_type.lower()}' in ('all', 'row', 'data') 
                        and '{exception_msg}' = '' then
                     named_struct(
                        'missing_in_source', {data_reconcile_output.missing_in_src_count},
                        'missing_in_target', {data_reconcile_output.missing_in_tgt_count}
                    ) else null end,
                    'column_comparison', case when '{self.report_type.lower()}' in ('all', 'data') 
                        and '{exception_msg}' = '' then
                    named_struct(
                        'absolute_mismatch', {data_reconcile_output.mismatch_count},
                        'threshold_mismatch', {data_reconcile_output.threshold_output.threshold_mismatch_count},
                        'mismatch_columns', '{",".join(mismatch_columns)}'
                    ) else null end,
                    'schema_comparison', case when '{self.report_type.lower()}' in ('all', 'schema') 
                        and '{exception_msg}' = '' then
                        {schema_reconcile_output.is_valid} else null end
                ) as recon_metrics,
                named_struct(
                    'status', {status}, 
                    'run_by_user', '{self.ws.current_user.me().user_name}', 
                    'exception_message', "{exception_msg}"
                ) as run_metrics,
                cast('{insertion_time}' as timestamp) as inserted_ts
            """
        )
        _write_df_to_delta(df, f"{self._db_prefix}.{_RECON_METRICS_TABLE_NAME}")

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
        df = df.limit(_SAMPLE_ROWS).select(create_map(*map_args).alias("data"))
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
        _write_df_to_delta(df, f"{self._db_prefix}.{_RECON_DETAILS_TABLE_NAME}")

    def _insert_into_details_table(
        self,
        recon_table_id: int,
        reconcile_output: DataReconcileOutput,
        schema_output: SchemaReconcileOutput,
    ):
        if reconcile_output.mismatch_count > 0 and reconcile_output.mismatch.mismatch_df:
            self._create_map_column_and_insert(
                recon_table_id,
                reconcile_output.mismatch.mismatch_df,
                "mismatch",
                False,
            )

        if reconcile_output.missing_in_src_count > 0 and reconcile_output.missing_in_src:
            self._create_map_column_and_insert(
                recon_table_id,
                reconcile_output.missing_in_src,
                "missing_in_source",
                False,
            )

        if reconcile_output.missing_in_tgt_count > 0 and reconcile_output.missing_in_tgt:
            self._create_map_column_and_insert(
                recon_table_id,
                reconcile_output.missing_in_tgt,
                "missing_in_target",
                False,
            )

        if (
            reconcile_output.threshold_output.threshold_mismatch_count > 0
            and reconcile_output.threshold_output.threshold_df
        ):
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
