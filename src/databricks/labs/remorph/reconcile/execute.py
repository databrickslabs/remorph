import logging
from datetime import datetime
from uuid import uuid4

from pyspark.errors import PySparkException
from pyspark.sql import DataFrame, SparkSession
from sqlglot import Dialect

from databricks.labs.remorph.config import DatabaseConfig, TableRecon, get_dialect
from databricks.labs.remorph.reconcile.compare import (
    capture_mismatch_data_and_columns,
    reconcile_data,
)
from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.connectors.source_adapter import create_adapter
from databricks.labs.remorph.reconcile.exception import (
    DataSourceRuntimeException,
    InvalidInputException,
)
from databricks.labs.remorph.reconcile.query_builder.hash_query import HashQueryBuilder
from databricks.labs.remorph.reconcile.query_builder.sampling_query import (
    SamplingQueryBuilder,
)
from databricks.labs.remorph.reconcile.query_builder.threshold_query import (
    ThresholdQueryBuilder,
)
from databricks.labs.remorph.reconcile.recon_capture import (
    ReconCapture,
    generate_final_reconcile_output,
)
from databricks.labs.remorph.reconcile.recon_config import (
    DataReconcileOutput,
    ReconcileOutput,
    ReconcileProcessDuration,
    Schema,
    SchemaReconcileOutput,
    Table,
    ThresholdOutput,
)
from databricks.labs.remorph.reconcile.schema_compare import SchemaCompare
from databricks.labs.remorph.transpiler.execute import verify_workspace_client
from databricks.sdk import WorkspaceClient

logger = logging.getLogger(__name__)
_SAMPLE_ROWS = 50


def validate_input(input_value: str, list_of_value: set, message: str):
    if input_value not in list_of_value:
        error_message = f"{message} --> {input_value} is not one of {list_of_value}"
        logger.error(error_message)
        raise InvalidInputException(error_message)


def recon(
    ws: WorkspaceClient,
    spark: SparkSession,
    table_recon: TableRecon,
    source_dialect: Dialect,
    report_type: str,
) -> ReconcileOutput:
    """[EXPERIMENTAL] Reconcile the data between the source and target tables."""
    # verify the workspace client and add proper product and version details
    # TODO For now we are utilising the
    #  verify_workspace_client from transpile/execute.py file. Later verify_workspace_client function has to be
    #  refactored

    ws_client: WorkspaceClient = verify_workspace_client(ws)

    # validate the report type
    report_type = report_type.lower()
    logger.info(report_type)
    validate_input(report_type, {"schema", "data", "row", "all"}, "Invalid report type")

    database_config = DatabaseConfig(
        source_catalog=table_recon.source_catalog,
        source_schema=table_recon.source_schema,
        target_catalog=table_recon.target_catalog,
        target_schema=table_recon.target_schema,
    )

    source, target = initialise_data_source(
        engine=source_dialect,
        spark=spark,
        ws=ws_client,
        secret_scope="secret_scope",
    )

    recon_id = str(uuid4())
    # initialise the Reconciliation
    reconciler = Reconciliation(
        source,
        target,
        database_config,
        report_type,
        SchemaCompare(spark=spark),
        source_dialect,
    )

    # initialise the recon capture class
    recon_capture = ReconCapture(
        database_config=database_config,
        recon_id=recon_id,
        report_type=report_type,
        source_dialect=source_dialect,
        ws=ws_client,
        spark=spark,
    )

    for table_conf in table_recon.tables:
        recon_process_duration = ReconcileProcessDuration(start_ts=str(datetime.now()), end_ts=None)
        schema_reconcile_output = SchemaReconcileOutput(is_valid=True)
        data_reconcile_output = DataReconcileOutput()
        try:
            src_schema, tgt_schema = _get_schema(
                source=source, target=target, table_conf=table_conf, database_config=database_config
            )
        except DataSourceRuntimeException as e:
            schema_reconcile_output = SchemaReconcileOutput(is_valid=False, exception=str(e))
        else:
            if report_type in {"schema", "all"}:
                schema_reconcile_output = _run_reconcile_schema(
                    reconciler=reconciler, table_conf=table_conf, src_schema=src_schema, tgt_schema=tgt_schema
                )

            if report_type in {"data", "row", "all"}:
                data_reconcile_output = _run_reconcile_data(
                    reconciler=reconciler, table_conf=table_conf, src_schema=src_schema, tgt_schema=tgt_schema
                )

        recon_process_duration.end_ts = str(datetime.now())
        # Persist the data to the delta tables
        recon_capture.start(
            data_reconcile_output=data_reconcile_output,
            schema_reconcile_output=schema_reconcile_output,
            table_conf=table_conf,
            recon_process_duration=recon_process_duration,
        )

    return generate_final_reconcile_output(recon_id=recon_id, spark=spark)


def initialise_data_source(
    ws: WorkspaceClient,
    spark: SparkSession,
    engine: Dialect,
    secret_scope: str,
):
    source = create_adapter(engine=engine, spark=spark, ws=ws, secret_scope=secret_scope)
    target = create_adapter(engine=get_dialect("databricks"), spark=spark, ws=ws, secret_scope=secret_scope)

    return source, target


def _get_missing_data(
    reader: DataSource,
    sampler: SamplingQueryBuilder,
    missing_df: DataFrame,
    catalog: str,
    schema: str,
    table_name: str,
) -> DataFrame:
    sample_query = sampler.build_query(missing_df)
    return reader.read_data(
        catalog=catalog,
        schema=schema,
        table=table_name,
        query=sample_query,
        options=None,
    )


class Reconciliation:

    def __init__(
        self,
        source: DataSource,
        target: DataSource,
        database_config: DatabaseConfig,
        report_type: str,
        schema_comparator: SchemaCompare,
        source_engine: Dialect,
    ):
        self._source = source
        self._target = target
        self._report_type = report_type
        self._source_catalog = database_config.source_catalog
        self._source_schema = database_config.source_schema
        self._target_catalog = database_config.target_catalog
        self._target_schema = database_config.target_schema
        self._schema_comparator = schema_comparator
        self._target_engine = get_dialect("databricks")
        self._source_engine = source_engine

    def reconcile_data(
        self,
        table_conf: Table,
        src_schema: list[Schema],
        tgt_schema: list[Schema],
    ) -> DataReconcileOutput:
        data_reconcile_output = self._get_reconcile_output(table_conf, src_schema, tgt_schema)
        reconcile_output = data_reconcile_output
        if self._report_type in {"data", "all"}:
            reconcile_output = self._get_sample_data(table_conf, data_reconcile_output, src_schema, tgt_schema)
            if table_conf.get_threshold_columns("source"):
                reconcile_output.threshold_output = self._reconcile_threshold_data(table_conf, src_schema, tgt_schema)

        if self._report_type == "row" and table_conf.get_threshold_columns("source"):
            logger.warning("Threshold comparison is ignored for 'row' report type")

        return reconcile_output

    def reconcile_schema(
        self,
        src_schema: list[Schema],
        tgt_schema: list[Schema],
        table_conf: Table,
    ):
        return self._schema_comparator.compare(src_schema, tgt_schema, self._source_engine, table_conf)

    def _get_reconcile_output(
        self,
        table_conf,
        src_schema,
        tgt_schema,
    ):
        src_hash_query = HashQueryBuilder(table_conf, src_schema, "source", self._source_engine).build_query(
            report_type=self._report_type
        )
        tgt_hash_query = HashQueryBuilder(table_conf, tgt_schema, "target", self._target_engine).build_query(
            report_type=self._report_type
        )
        src_data = self._source.read_data(
            catalog=self._source_catalog,
            schema=self._source_schema,
            table=table_conf.source_name,
            query=src_hash_query,
            options=table_conf.jdbc_reader_options,
        )
        tgt_data = self._target.read_data(
            catalog=self._target_catalog,
            schema=self._target_schema,
            table=table_conf.target_name,
            query=tgt_hash_query,
            options=table_conf.jdbc_reader_options,
        )

        return reconcile_data(
            source=src_data, target=tgt_data, key_columns=table_conf.join_columns, report_type=self._report_type
        )

    def _get_sample_data(
        self,
        table_conf,
        reconcile_output,
        src_schema,
        tgt_schema,
    ):
        mismatch = None
        missing_in_src = None
        missing_in_tgt = None

        if (
            reconcile_output.mismatch_count > 0
            or reconcile_output.missing_in_src_count > 0
            or reconcile_output.missing_in_tgt_count > 0
        ):
            src_sampler = SamplingQueryBuilder(table_conf, src_schema, "source", self._source_engine)
            tgt_sampler = SamplingQueryBuilder(table_conf, tgt_schema, "target", self._target_engine)
            if reconcile_output.mismatch_count > 0:
                mismatch = self._get_mismatch_data(
                    src_sampler,
                    tgt_sampler,
                    reconcile_output.mismatch.mismatch_df,
                    table_conf.join_columns,
                    table_conf.source_name,
                    table_conf.target_name,
                )

            if reconcile_output.missing_in_src_count > 0:
                missing_in_src = _get_missing_data(
                    self._target,
                    tgt_sampler,
                    reconcile_output.missing_in_src,
                    self._target_catalog,
                    self._target_schema,
                    table_conf.target_name,
                )

            if reconcile_output.missing_in_tgt_count > 0:
                missing_in_tgt = _get_missing_data(
                    self._source,
                    src_sampler,
                    reconcile_output.missing_in_tgt,
                    self._source_catalog,
                    self._source_schema,
                    table_conf.source_name,
                )

        return DataReconcileOutput(
            mismatch=mismatch,
            mismatch_count=reconcile_output.mismatch_count,
            missing_in_src_count=reconcile_output.missing_in_src_count,
            missing_in_tgt_count=reconcile_output.missing_in_tgt_count,
            missing_in_src=missing_in_src,
            missing_in_tgt=missing_in_tgt,
        )

    def _get_mismatch_data(
        self,
        src_sampler,
        tgt_sampler,
        mismatch,
        key_columns,
        src_table: str,
        tgt_table: str,
    ):
        src_mismatch_sample_query = src_sampler.build_query(mismatch)
        tgt_mismatch_sample_query = tgt_sampler.build_query(mismatch)

        src_data = self._source.read_data(
            catalog=self._source_catalog,
            schema=self._source_schema,
            table=src_table,
            query=src_mismatch_sample_query,
            options=None,
        )
        tgt_data = self._target.read_data(
            catalog=self._target_catalog,
            schema=self._target_schema,
            table=tgt_table,
            query=tgt_mismatch_sample_query,
            options=None,
        )

        return capture_mismatch_data_and_columns(source=src_data, target=tgt_data, key_columns=key_columns)

    def _reconcile_threshold_data(
        self,
        table_conf: Table,
        src_schema: list[Schema],
        tgt_schema: list[Schema],
    ):

        src_data, tgt_data = self._get_threshold_data(table_conf, src_schema, tgt_schema)

        source_view = f"source_{table_conf.source_name}_df_threshold_vw"
        target_view = f"target_{table_conf.target_name}_df_threshold_vw"

        src_data.createOrReplaceTempView(source_view)
        tgt_data.createOrReplaceTempView(target_view)

        return self._compute_threshold_comparison(table_conf, src_schema)

    def _get_threshold_data(
        self,
        table_conf: Table,
        src_schema: list[Schema],
        tgt_schema: list[Schema],
    ) -> tuple[DataFrame, DataFrame]:
        src_threshold_query = ThresholdQueryBuilder(
            table_conf, src_schema, "source", self._source_engine
        ).build_threshold_query()
        tgt_threshold_query = ThresholdQueryBuilder(
            table_conf, tgt_schema, "target", self._target_engine
        ).build_threshold_query()

        src_data = self._source.read_data(
            catalog=self._source_catalog,
            schema=self._source_schema,
            table=table_conf.source_name,
            query=src_threshold_query,
            options=table_conf.jdbc_reader_options,
        )
        tgt_data = self._target.read_data(
            catalog=self._target_catalog,
            schema=self._target_schema,
            table=table_conf.target_name,
            query=tgt_threshold_query,
            options=table_conf.jdbc_reader_options,
        )

        return src_data, tgt_data

    def _compute_threshold_comparison(self, table_conf: Table, src_schema: list[Schema]) -> ThresholdOutput:
        threshold_comparison_query = ThresholdQueryBuilder(
            table_conf, src_schema, "target", self._target_engine
        ).build_comparison_query()

        threshold_result = self._target.read_data(
            catalog=self._target_catalog,
            schema=self._target_schema,
            table=table_conf.target_name,
            query=threshold_comparison_query,
            options=table_conf.jdbc_reader_options,
        )
        threshold_columns = table_conf.get_threshold_columns("source")
        failed_where_cond = " OR ".join([name + "_match = 'Failed'" for name in threshold_columns])
        mismatched_df = threshold_result.filter(failed_where_cond)
        mismatched_count = mismatched_df.count()
        threshold_df = None
        if mismatched_count > 0:
            threshold_df = mismatched_df.limit(_SAMPLE_ROWS)

        return ThresholdOutput(threshold_df=threshold_df, threshold_mismatch_count=mismatched_count)


def _get_schema(
    source: DataSource,
    target: DataSource,
    table_conf: Table,
    database_config: DatabaseConfig,
) -> tuple[list[Schema], list[Schema]]:

    src_schema = source.get_schema(
        catalog=database_config.source_catalog,
        schema=database_config.source_schema,
        table=table_conf.source_name,
    )
    tgt_schema = target.get_schema(
        catalog=database_config.target_catalog,
        schema=database_config.target_schema,
        table=table_conf.target_name,
    )

    return src_schema, tgt_schema


def _run_reconcile_data(
    reconciler: Reconciliation,
    table_conf: Table,
    src_schema: list[Schema],
    tgt_schema: list[Schema],
) -> DataReconcileOutput:
    try:
        return reconciler.reconcile_data(table_conf=table_conf, src_schema=src_schema, tgt_schema=tgt_schema)
    except DataSourceRuntimeException as e:
        return DataReconcileOutput(exception=str(e))


def _run_reconcile_schema(
    reconciler: Reconciliation,
    table_conf: Table,
    src_schema: list[Schema],
    tgt_schema: list[Schema],
):
    try:
        return reconciler.reconcile_schema(table_conf=table_conf, src_schema=src_schema, tgt_schema=tgt_schema)
    except PySparkException as e:
        return SchemaReconcileOutput(is_valid=False, exception=str(e))
