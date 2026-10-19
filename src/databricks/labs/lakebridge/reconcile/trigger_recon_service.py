"""Reconcile orchestration."""

import contextlib
import logging
from datetime import datetime, timezone
from uuid import uuid4

from databricks.sdk import WorkspaceClient
from pyspark.errors import PySparkException
from pyspark.sql import SparkSession

from databricks.labs.lakebridge.config import (
    ReconcileConfig,
    SourceConnectionConfig,
    TableRecon,
    TargetConnectionConfig,
)
from databricks.labs.lakebridge.reconcile import utils
from databricks.labs.lakebridge.reconcile.connectors.data_source import DataSource
from databricks.labs.lakebridge.reconcile.constants import RECON_SAMPLE_VIEW_PREFIX
from databricks.labs.lakebridge.reconcile.exception import DataSourceRuntimeException, ReconciliationException
from databricks.labs.lakebridge.reconcile.fingerprint.exceptions import (
    FingerprintError,
    UnmappedTargetColumnMappingError,
)
from databricks.labs.lakebridge.reconcile.fingerprint.metadata import (
    INELIGIBLE_UNMAPPED_TARGET_COLUMN_MAPPING,
    FingerprintRunMetadata,
)
from databricks.labs.lakebridge.reconcile.fingerprint.orchestrator import (
    ConnectionConfigPair,
    FingerprintResult,
    build_mismatch_output,
    classify_ineligibility,
    fingerprint_match_output,
    resolve_compare_key_columns,
    run_fingerprint_precheck,
)
from databricks.labs.lakebridge.reconcile.normalize_recon_config_service import NormalizeReconConfigService
from databricks.labs.lakebridge.reconcile.recon_capture import (
    ReconCapture,
    ReconIntermediatePersist,
    generate_final_reconcile_output,
)
from databricks.labs.lakebridge.reconcile.recon_config import Schema, Table
from databricks.labs.lakebridge.reconcile.recon_output_config import (
    DataReconcileOutput,
    ReconcileOutput,
    ReconcileProcessDuration,
    ReconcileTableOutput,
    SchemaReconcileOutput,
)
from databricks.labs.lakebridge.reconcile.reconciliation import Reconciliation
from databricks.labs.lakebridge.reconcile.schema_compare import SchemaCompare
from databricks.labs.lakebridge.transpiler.execute import verify_workspace_client
from databricks.labs.lakebridge.transpiler.sqlglot.dialect_utils import get_dialect

logger = logging.getLogger(__name__)
_RECON_REPORT_TYPES = {"schema", "data", "row", "all", "aggregate"}


def _try_unpersist(df) -> None:
    """Best-effort ``unpersist`` for cached fingerprint frames on a fallback
    exit. The DataFrames may have been ``persist()``-ed by
    ``compute_target_fingerprint`` / source-side fetch and we don't want them
    to linger in executor storage for the rest of the recon.
    """
    if df is None:
        return
    with contextlib.suppress(Exception):
        df.unpersist(blocking=False)


def drop_sample_temp_views(spark: SparkSession) -> None:
    """Drop the per-call sampling temp views (RECON_SAMPLE_VIEW_PREFIX) left by the Databricks
    sampling path. Uses SHOW VIEWS (metadata-only) rather than spark.catalog.listTables(), which
    resolves every table in the current schema and fails if any can't be loaded. Best-effort and
    pattern-scoped: only session temp views carrying our prefix are removed; a cleanup failure
    must not fail the reconcile run.
    """
    try:
        temp_views = spark.sql("SHOW VIEWS").where("isTemporary = true").collect()
        for row in temp_views:
            name = row["viewName"]
            if name.startswith(RECON_SAMPLE_VIEW_PREFIX):
                spark.sql(f"DROP VIEW IF EXISTS {name}")
                logger.info(f"Dropped sampling temp view {name}")
    except PySparkException:
        logger.exception("Cleaning sampling temp views failed. Resuming program")


class TriggerReconService:

    @staticmethod
    def trigger_recon(
        ws: WorkspaceClient,
        spark: SparkSession,
        table_recon: TableRecon,
        reconcile_config: ReconcileConfig,
    ) -> ReconcileOutput:
        reconciler, recon_capture = TriggerReconService.create_recon_dependencies(ws, spark, reconcile_config)
        recon_capture.store_run_context(reconcile_config, table_recon)

        try:
            for table_conf in table_recon.tables:
                try:
                    TriggerReconService.recon_one(reconciler, recon_capture, reconcile_config, table_conf)
                finally:
                    drop_sample_temp_views(spark)

            return TriggerReconService.verify_successful_reconciliation(
                generate_final_reconcile_output(
                    recon_id=recon_capture.recon_id,
                    spark=spark,
                    metadata_config=reconcile_config.metadata_config,
                ),
                reconcile_config.report_type,
            )
        finally:
            try:
                ws.dbfs.delete(str(reconciler.intermediate_persist.base_dir), recursive=True)
            except IOError:
                logger.exception("Cleaning intermediate storage failed. Resuming program")

    @staticmethod
    def create_recon_dependencies(
        ws: WorkspaceClient, spark: SparkSession, reconcile_config: ReconcileConfig
    ) -> tuple[Reconciliation, ReconCapture]:
        ws_client: WorkspaceClient = verify_workspace_client(ws)

        # validate the report type
        report_type = reconcile_config.report_type.lower()
        source_dialect = reconcile_config.source.dialect
        logger.info(f"report_type: {report_type}, data_source: {source_dialect} ")
        utils.validate_input(report_type, _RECON_REPORT_TYPES, "Invalid report type")

        # validate the connection
        source, target = utils.initialise_data_source(
            source_dialect=reconcile_config.source.dialect,
            spark=spark,
            connection_name=reconcile_config.source.uc_connection_name,
        )

        recon_id = uuid4().hex
        # initialise the Reconciliation
        reconciler = Reconciliation(
            source,
            target,
            reconcile_config.source,
            reconcile_config.target,
            report_type,
            SchemaCompare(spark=spark),
            get_dialect(source_dialect),
            spark,
            metadata_config=reconcile_config.metadata_config,
            intermediate_persist=ReconIntermediatePersist(spark, reconcile_config.metadata_config),
            hash_expression_overrides=reconcile_config.hash_expression_overrides,
        )

        recon_capture = ReconCapture(
            source_connection=reconcile_config.source,
            target_connection=reconcile_config.target,
            recon_id=recon_id,
            report_type=report_type,
            source_dialect=get_dialect(source_dialect),
            ws=ws_client,
            spark=spark,
            metadata_config=reconcile_config.metadata_config,
        )

        return reconciler, recon_capture

    @staticmethod
    def recon_one(
        reconciler: Reconciliation,
        recon_capture: ReconCapture,
        reconcile_config: ReconcileConfig,
        table_conf: Table,
    ) -> tuple[SchemaReconcileOutput, DataReconcileOutput]:
        normalized_table_conf = NormalizeReconConfigService(
            reconciler.source, reconciler.target
        ).normalize_recon_table_config(table_conf)

        (
            schema_reconcile_output,
            data_reconcile_output,
            recon_process_duration,
            fingerprint_metadata,
        ) = TriggerReconService.do_recon_one(
            reconciler, reconcile_config, normalized_table_conf, recon_id=recon_capture.recon_id
        )

        recon_capture.start(
            data_reconcile_output=data_reconcile_output,
            schema_reconcile_output=schema_reconcile_output,
            table_conf=table_conf,
            recon_process_duration=recon_process_duration,
            record_count=reconciler.get_record_count(table_conf, reconciler.report_type),
            fingerprint_metadata=fingerprint_metadata,
        )

        return schema_reconcile_output, data_reconcile_output

    @staticmethod
    def do_recon_one(
        reconciler: Reconciliation,
        reconcile_config: ReconcileConfig,
        table_conf: Table,
        *,
        recon_id: str | None = None,
    ):
        recon_process_duration = ReconcileProcessDuration(start_ts=str(datetime.now(tz=timezone.utc)), end_ts=None)
        schema_reconcile_output = SchemaReconcileOutput(is_valid=True)
        data_reconcile_output = DataReconcileOutput()

        ineligibility_reason = classify_ineligibility(
            flag_enabled=reconcile_config.reconcile_optimizer,
            data_source=reconcile_config.source.dialect,
            report_type=reconciler.report_type,
            table_conf=table_conf,
        )
        if ineligibility_reason is not None:
            fingerprint_metadata: FingerprintRunMetadata = FingerprintRunMetadata.ineligible(ineligibility_reason)
        else:
            fingerprint_metadata = FingerprintRunMetadata(eligible=True)

        try:
            src_schema, tgt_schema = TriggerReconService.get_schemas(
                reconciler.source, reconciler.target, table_conf, reconcile_config.source, reconcile_config.target, True
            )
        except DataSourceRuntimeException as e:
            schema_reconcile_output = SchemaReconcileOutput(is_valid=False, exception=str(e))
            if ineligibility_reason is None:
                fingerprint_metadata = FingerprintRunMetadata(
                    eligible=True, fallback_to_full_pipeline=True, verdict="FAILED"
                )
        else:
            if reconciler.report_type in {"schema", "all"}:
                schema_reconcile_output = TriggerReconService._run_reconcile_schema(
                    reconciler=reconciler,
                    table_conf=table_conf,
                    src_schema=src_schema,
                    tgt_schema=tgt_schema,
                )
                logger.info("Schema comparison is completed.")

            if reconciler.report_type in {"data", "row", "all"}:
                data_reconcile_output, fingerprint_metadata = TriggerReconService.run_fingerprint_or_reconcile_data(
                    reconciler=reconciler,
                    reconcile_config=reconcile_config,
                    table_conf=table_conf,
                    src_schema=src_schema,
                    tgt_schema=tgt_schema,
                    ineligibility_reason=ineligibility_reason,
                    recon_id=recon_id,
                )
                logger.info(f"Reconciliation for '{reconciler.report_type}' report completed.")

        recon_process_duration.end_ts = str(datetime.now(tz=timezone.utc))
        return schema_reconcile_output, data_reconcile_output, recon_process_duration, fingerprint_metadata

    @staticmethod
    def get_schemas(
        source: DataSource,
        target: DataSource,
        table_conf: Table,
        source_connection: SourceConnectionConfig,
        target_connection: TargetConnectionConfig,
        normalize: bool,
    ) -> tuple[list[Schema], list[Schema]]:
        src_schema = source.get_schema(
            catalog=source_connection.catalog,
            schema=source_connection.schema,
            table=table_conf.source_name,
            normalize=normalize,
        )

        tgt_schema = target.get_schema(
            catalog=target_connection.catalog,
            schema=target_connection.schema,
            table=table_conf.target_name,
            normalize=normalize,
        )

        return src_schema, tgt_schema

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def _invoke_precheck(
        *,
        reconciler: Reconciliation,
        reconcile_config: ReconcileConfig,
        table_conf: Table,
        src_schema: list[Schema],
        tgt_schema: list[Schema],
        recon_id: str | None,
    ) -> tuple[FingerprintResult | None, str | None, bool]:
        """Run ``run_fingerprint_precheck`` and classify the outcome for the caller."""
        try:
            fp_result = run_fingerprint_precheck(
                source=reconciler.source,
                target=reconciler.target,
                spark=reconciler.spark,
                source_engine=reconciler.source_engine,
                connections=ConnectionConfigPair(source=reconcile_config.source, target=reconcile_config.target),
                table_conf=table_conf,
                src_schema=src_schema,
                tgt_schema=tgt_schema,
                report_type=reconciler.report_type,
                data_source=reconcile_config.source.dialect,
                recon_id=recon_id,
            )
        except UnmappedTargetColumnMappingError as e:
            logger.warning(f"Fingerprint precheck ineligible — {e}; falling back to full pipeline.")
            return None, INELIGIBLE_UNMAPPED_TARGET_COLUMN_MAPPING, False
        except (FingerprintError, DataSourceRuntimeException, PySparkException) as e:
            logger.warning(f"Fingerprint precheck failed ({e}); falling back to full pipeline.")
            return None, None, True
        except (KeyboardInterrupt, SystemExit, GeneratorExit):
            raise
        except BaseException as e:
            logger.warning(
                f"Fingerprint precheck raised an unexpected {type(e).__name__} ({e}); "
                "falling back to full pipeline.",
                exc_info=True,
            )
            return None, None, True
        return fp_result, None, False

    @staticmethod
    def run_fingerprint_or_reconcile_data(
        reconciler: Reconciliation,
        reconcile_config: ReconcileConfig,
        table_conf: Table,
        src_schema: list[Schema],
        tgt_schema: list[Schema],
        ineligibility_reason: str | None = None,
        recon_id: str | None = None,
    ) -> tuple[DataReconcileOutput, FingerprintRunMetadata]:
        """Try the fingerprint precheck; on any non-MATCH outcome, fall back to the
        full hash-and-join reconcile path.
        """
        if ineligibility_reason is None:
            ineligibility_reason = classify_ineligibility(
                flag_enabled=reconcile_config.reconcile_optimizer,
                data_source=reconcile_config.source.dialect,
                report_type=reconciler.report_type,
                table_conf=table_conf,
            )

        if ineligibility_reason is not None:
            data_reconcile_output = TriggerReconService._run_reconcile_data(
                reconciler=reconciler,
                table_conf=table_conf,
                src_schema=src_schema,
                tgt_schema=tgt_schema,
            )
            return data_reconcile_output, FingerprintRunMetadata.ineligible(ineligibility_reason)

        fp_result, runtime_ineligibility, precheck_failed = TriggerReconService._invoke_precheck(
            reconciler=reconciler,
            reconcile_config=reconcile_config,
            table_conf=table_conf,
            src_schema=src_schema,
            tgt_schema=tgt_schema,
            recon_id=recon_id,
        )

        if runtime_ineligibility is not None:
            data_reconcile_output = TriggerReconService._run_reconcile_data(
                reconciler=reconciler,
                table_conf=table_conf,
                src_schema=src_schema,
                tgt_schema=tgt_schema,
            )
            return data_reconcile_output, FingerprintRunMetadata.ineligible(runtime_ineligibility)

        if fp_result is None:
            data_reconcile_output = TriggerReconService._run_reconcile_data(
                reconciler=reconciler,
                table_conf=table_conf,
                src_schema=src_schema,
                tgt_schema=tgt_schema,
            )
            return data_reconcile_output, FingerprintRunMetadata.fallback(
                verdict="FAILED" if precheck_failed else None,
            )

        if fp_result.verdict == "MATCH":
            return fingerprint_match_output(), FingerprintRunMetadata.from_result(fp_result, verdict="MATCH")

        if fp_result.source_rows is None or fp_result.target_rows is None:
            _try_unpersist(fp_result.source_rows)
            _try_unpersist(fp_result.target_rows)
            data_reconcile_output = TriggerReconService._run_reconcile_data(
                reconciler=reconciler,
                table_conf=table_conf,
                src_schema=src_schema,
                tgt_schema=tgt_schema,
            )
            return data_reconcile_output, FingerprintRunMetadata.from_result(
                fp_result, verdict="MISMATCH", fallback_to_full_pipeline=True
            )

        try:
            data_reconcile_output = build_mismatch_output(
                src_hashed=fp_result.source_rows,
                tgt_hashed=fp_result.target_rows,
                key_columns=resolve_compare_key_columns(table_conf),
                report_type=reconciler.report_type,
                persistence=reconciler.intermediate_persist,
                max_sample_size=table_conf.get_max_sample_size(),
            )
        except (KeyboardInterrupt, SystemExit, GeneratorExit):
            raise
        except BaseException as e:
            _try_unpersist(fp_result.source_rows)
            _try_unpersist(fp_result.target_rows)
            logger.warning(
                f"Fingerprint mismatch-output build raised {type(e).__name__} ({e}); falling back to full pipeline.",
                exc_info=True,
            )
            data_reconcile_output = TriggerReconService._run_reconcile_data(
                reconciler=reconciler,
                table_conf=table_conf,
                src_schema=src_schema,
                tgt_schema=tgt_schema,
            )
            return data_reconcile_output, FingerprintRunMetadata.from_result(
                fp_result, verdict="MISMATCH", fallback_to_full_pipeline=True
            )
        return data_reconcile_output, FingerprintRunMetadata.from_result(fp_result, verdict="MISMATCH")

    @staticmethod
    def verify_successful_reconciliation(reconcile_output: ReconcileOutput, report_type: str) -> ReconcileOutput:
        def is_table_recon_mismatch(table_output: ReconcileTableOutput):
            is_mismatch = (
                table_output.status.column is False
                or table_output.status.row is False
                or table_output.status.schema is False
                or table_output.status.aggregate is False
            )
            if is_mismatch:
                logger.debug(
                    f"Mismatches found between source and target tables:"
                    f" ({table_output.source_table_name}, {table_output.target_table_name})."
                )

            return is_mismatch

        exceptions = [r for r in reconcile_output.results if r.exception_message]
        mismatched = [r for r in reconcile_output.results if is_table_recon_mismatch(r)]

        total_count, exc_count, mismatched_count = (len(reconcile_output.results), len(exceptions), len(mismatched))
        success_count = max(0, total_count - exc_count + mismatched_count)

        logger.info(
            f"Reconciliation **{report_type}** with id: {reconcile_output.recon_id} ran for total {total_count} source tables and their targets."
            f" {success_count} tables succeeded, {exc_count} tables failed with exceptions and {mismatched_count} tables mismatched."
        )

        if exceptions:
            raise ReconciliationException(
                f"Reconciliation **{report_type}** with id: {reconcile_output.recon_id} failed with exceptions for {exc_count} table(s). Please check recon metrics for details.",
                reconcile_output=reconcile_output,
            )

        if mismatched:
            logger.error(
                f"Reconciliation **{report_type}** with id: {reconcile_output.recon_id} found mismatches in {mismatched_count} table(s). Please check recon metrics for details."
            )
        else:
            logger.info(
                f"Reconciliation **{report_type}** with id: {reconcile_output.recon_id} completed successfully. Please check recon metrics for details."
            )

        return reconcile_output
