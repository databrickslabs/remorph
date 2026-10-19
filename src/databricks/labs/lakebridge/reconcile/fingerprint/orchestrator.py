import logging
import time
from dataclasses import dataclass

from pyspark.sql import DataFrame, SparkSession
from sqlglot import Dialect

from databricks.labs.lakebridge.config import SourceConnectionConfig, TargetConnectionConfig
from databricks.labs.lakebridge.reconcile.compare import (
    _HASH_COLUMN_NAME,
    capture_mismatch_data_and_columns,
)
from databricks.labs.lakebridge.reconcile.compare import (
    reconcile_data as compare_reconcile_data,
)
from databricks.labs.lakebridge.reconcile.connectors.data_source import DataSource
from databricks.labs.lakebridge.reconcile.connectors.dialect_utils import DialectUtils
from databricks.labs.lakebridge.reconcile.constants import DEFAULT_SAMPLE_ROWS
from databricks.labs.lakebridge.reconcile.fingerprint.columns import pair_detection_columns
from databricks.labs.lakebridge.reconcile.fingerprint.constants import pick_sub_bucket_count
from databricks.labs.lakebridge.reconcile.fingerprint.engine import (
    DetectionResult,
    DetectionVerdict,
    detect_and_solve,
)
from databricks.labs.lakebridge.reconcile.fingerprint.exceptions import (
    UnmappedTargetColumnMappingError,
    UnsupportedDataSourceError,
)
from databricks.labs.lakebridge.reconcile.fingerprint.metadata import (
    FETCH_PATH_V1_SANDWICH,
    INELIGIBLE_COLUMN_THRESHOLDS_CONFIGURED,
    INELIGIBLE_FILTERS_CONFIGURED,
    INELIGIBLE_FLAG_DISABLED,
    INELIGIBLE_NO_JOIN_COLUMNS,
    INELIGIBLE_REPORT_TYPE_NOT_DATA,
    INELIGIBLE_TABLE_THRESHOLDS_CONFIGURED,
    INELIGIBLE_TRANSFORMS_CONFIGURED,
    INELIGIBLE_UNSUPPORTED_DIALECT,
)
from databricks.labs.lakebridge.reconcile.fingerprint.query_builders.base import FingerprintQueryBuilder
from databricks.labs.lakebridge.reconcile.fingerprint.query_builders.redshift import RedshiftFingerprintQueryBuilder
from databricks.labs.lakebridge.reconcile.fingerprint.row_count import fetch_target_row_count
from databricks.labs.lakebridge.reconcile.fingerprint.spark_target import (
    build_target_filter_subquery,
    compute_target_fingerprint,
)
from databricks.labs.lakebridge.reconcile.query_builder.column_transformer import (
    ReconcileLayer,
    RuleBasedColumnTransformer,
)
from databricks.labs.lakebridge.reconcile.query_builder.hash_query import HashQueryBuilder
from databricks.labs.lakebridge.reconcile.recon_capture import AbstractReconIntermediatePersist
from databricks.labs.lakebridge.reconcile.recon_config import Schema, Table
from databricks.labs.lakebridge.reconcile.recon_output_config import (
    DataReconcileOutput,
    MismatchOutput,
)
from databricks.labs.lakebridge.transpiler.sqlglot.dialect_utils import get_dialect

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ColumnAlignment:
    column_mapping: dict[str, str] | None


@dataclass(frozen=True)
class FingerprintResult:
    verdict: DetectionVerdict
    source_rows: DataFrame | None = None
    target_rows: DataFrame | None = None
    solved_count: int = 0
    unsolved_sb_count: int = 0
    total_mismatched_sbs: int = 0
    detection_elapsed_ms: int = 0
    sub_bucket_count: int = 0
    bucket_count: int = 0
    target_row_count: int | None = None
    row_count_source: str | None = None
    fetch_path: str | None = None


@dataclass(frozen=True)
class TierSelection:
    """Adaptive (sub_bucket_count, bucket_count) for one run."""

    sub_bucket_count: int
    bucket_count: int
    target_row_count: int | None
    row_count_source: str


def classify_ineligibility(
    *,
    flag_enabled: bool,
    data_source: str,
    report_type: str,
    table_conf: Table,
) -> str | None:
    """Return the ineligibility reason for the pre-check, or None when eligible."""
    if not flag_enabled:
        return INELIGIBLE_FLAG_DISABLED
    if data_source not in fingerprint_supported_sources():
        return INELIGIBLE_UNSUPPORTED_DIALECT
    if report_type not in {"data", "row", "all"}:
        return INELIGIBLE_REPORT_TYPE_NOT_DATA
    if not table_conf.join_columns:
        return INELIGIBLE_NO_JOIN_COLUMNS
    if table_conf.filters and (table_conf.filters.source or table_conf.filters.target):
        return INELIGIBLE_FILTERS_CONFIGURED
    if table_conf.transformations:
        return INELIGIBLE_TRANSFORMS_CONFIGURED
    if table_conf.column_thresholds:
        return INELIGIBLE_COLUMN_THRESHOLDS_CONFIGURED
    if table_conf.table_thresholds:
        return INELIGIBLE_TABLE_THRESHOLDS_CONFIGURED
    return None


def align_columns(
    table_conf: Table,
    src_schema: list[Schema],
    tgt_schema: list[Schema],
) -> ColumnAlignment | None:
    """Map a Table config to fingerprint column parameters, or raise/return None if ineligible."""
    del src_schema
    if table_conf.filters and (table_conf.filters.source or table_conf.filters.target):
        return None
    if table_conf.transformations:
        return None
    if table_conf.column_thresholds:
        return None
    if table_conf.table_thresholds:
        return None

    col_map = {
        DialectUtils.unnormalize_identifier(cm.source_name).lower(): DialectUtils.unnormalize_identifier(cm.target_name)
        for cm in table_conf.column_mapping or []
    }

    if col_map:
        tgt_cols_bare = {DialectUtils.unnormalize_identifier(s.ansi_normalized_column_name).lower() for s in tgt_schema}
        for src_name, tgt_name in col_map.items():
            if DialectUtils.unnormalize_identifier(tgt_name).lower() not in tgt_cols_bare:
                raise UnmappedTargetColumnMappingError(
                    f"column_mapping target {tgt_name!r} (mapped from {src_name!r}) "
                    f"not found in target schema for table {table_conf.source_name!r}"
                )

    return ColumnAlignment(
        column_mapping=col_map if col_map else None,
    )


def resolve_compare_key_columns(table_conf: Table) -> list[str]:
    """Return join columns for compare.reconcile_data."""
    return table_conf.join_columns or []


def fingerprint_match_output() -> DataReconcileOutput:
    """Zeroed DataReconcileOutput for a confirmed MATCH."""
    return DataReconcileOutput(
        mismatch_count=0,
        missing_in_src_count=0,
        missing_in_tgt_count=0,
        mismatch=MismatchOutput(),
        missing_in_src=None,
        missing_in_tgt=None,
    )


def build_mismatch_output(
    src_hashed: DataFrame,
    tgt_hashed: DataFrame,
    key_columns: list[str],
    report_type: str,
    persistence: AbstractReconIntermediatePersist,
    max_sample_size: int = DEFAULT_SAMPLE_ROWS,
) -> DataReconcileOutput:
    """Run compare.reconcile_data on rows that already have hash_value_recon."""
    cached_frames: list[DataFrame] = []
    if report_type in {"all", "data"}:
        if persistence.is_serverless:
            src_hashed = persistence.write_and_read_df_with_volumes(src_hashed)
            tgt_hashed = persistence.write_and_read_df_with_volumes(tgt_hashed)
        else:
            src_hashed = src_hashed.cache()
            tgt_hashed = tgt_hashed.cache()
            cached_frames = [src_hashed, tgt_hashed]

    try:
        output = compare_reconcile_data(
            source=src_hashed,
            target=tgt_hashed,
            key_columns=key_columns,
            report_type=report_type,
            persistence=persistence,
            max_sample_size=max_sample_size,
        )

        if report_type not in {"all", "data"} or output.mismatch_count == 0:
            return output

        return _backfill_mismatch_columns(src_hashed, tgt_hashed, key_columns, persistence, output, max_sample_size)
    finally:
        for df in cached_frames:
            df.unpersist(blocking=False)


def _backfill_mismatch_columns(
    src_hashed: DataFrame,
    tgt_hashed: DataFrame,
    key_columns: list[str],
    persistence: AbstractReconIntermediatePersist,
    output: DataReconcileOutput,
    max_sample_size: int,
) -> DataReconcileOutput:
    """Add ``mismatch_columns`` (and a genuine-mismatch row filter) to ``output`` for the
    fingerprint ``report_type='all'`` MISMATCH path, reusing the already-fetched frames.
    """
    src_for_capture = src_hashed.drop(_HASH_COLUMN_NAME) if _HASH_COLUMN_NAME in src_hashed.columns else src_hashed
    tgt_for_capture = tgt_hashed.drop(_HASH_COLUMN_NAME) if _HASH_COLUMN_NAME in tgt_hashed.columns else tgt_hashed

    common_cols = [c for c in src_for_capture.columns if c in set(tgt_for_capture.columns)]
    src_for_capture = src_for_capture.select(*common_cols)
    tgt_for_capture = tgt_for_capture.select(*common_cols)

    capture = capture_mismatch_data_and_columns(
        source=src_for_capture,
        target=tgt_for_capture,
        key_columns=key_columns,
        persistence=persistence,
        sample_size=max_sample_size,
    )

    return DataReconcileOutput(
        mismatch_count=output.mismatch_count,
        missing_in_src_count=output.missing_in_src_count,
        missing_in_tgt_count=output.missing_in_tgt_count,
        missing_in_src=output.missing_in_src,
        missing_in_tgt=output.missing_in_tgt,
        mismatch=MismatchOutput(
            mismatch_df=capture.mismatch_df,
            mismatch_columns=capture.mismatch_columns,
        ),
        threshold_output=output.threshold_output,
    )


def resolve_detection_columns(
    table_conf: Table,
    src_schema: list[Schema],
    source: DataSource,
    source_engine: Dialect,
) -> list[Schema] | None:
    """Resolve hash columns against the source schema, or None to skip fingerprint."""
    _src_layer = ReconcileLayer(source, source_engine, src_schema)
    _transformer = RuleBasedColumnTransformer(source=_src_layer, target=_src_layer, table_conf=table_conf)
    hash_col_names = HashQueryBuilder(
        table_conf, src_schema, "source", source_engine, source, _transformer
    ).ordered_hash_columns()
    if not hash_col_names:
        logger.warning("Fingerprint: no hash columns resolved — skipping")
        return None

    by_name = {DialectUtils.unnormalize_identifier(s.ansi_normalized_column_name).lower(): s for s in src_schema}
    detection_cols: list[Schema] = []
    for name in hash_col_names:
        schema_entry = by_name.get(DialectUtils.unnormalize_identifier(name).lower())
        if schema_entry is None:
            logger.warning(f"Fingerprint: hash column '{name}' missing from source schema — skipping")
            return None
        detection_cols.append(schema_entry)
    return detection_cols


def resolve_target_detection_columns(
    detection_cols: list[Schema],
    tgt_schema: list[Schema],
    column_mapping: dict[str, str] | None,
) -> list[Schema] | None:
    """Target-side counterpart of ``detection_cols``: for each source detection column, in the
    same source-canonical order, the matching TARGET ``Schema`` (physical name AND type).
    """
    tgt_by_name = {DialectUtils.unnormalize_identifier(s.ansi_normalized_column_name).lower(): s for s in tgt_schema}
    mapping = column_mapping or {}
    resolved: list[Schema] = []
    for src_col in detection_cols:
        src_bare = DialectUtils.unnormalize_identifier(src_col.ansi_normalized_column_name).lower()
        tgt_bare = mapping.get(src_bare, src_bare)
        entry = tgt_by_name.get(DialectUtils.unnormalize_identifier(tgt_bare).lower())
        if entry is None:
            logger.warning(
                f"Fingerprint: target column for source '{src_bare}' (target '{tgt_bare}') "
                "not found in target schema — skipping pre-check"
            )
            return None
        resolved.append(entry)
    return resolved


def select_tier(
    spark: SparkSession,
    target_connection: TargetConnectionConfig,
    table_conf: Table,
) -> TierSelection:
    """Pick (sub_bucket_count, bucket_count) from the target Delta row count."""
    row_count_result = fetch_target_row_count(
        spark,
        catalog=target_connection.catalog,
        schema=target_connection.schema,
        table=table_conf.target_name,
    )
    sub_bucket_count, bucket_count = pick_sub_bucket_count(row_count_result.row_count)
    return TierSelection(
        sub_bucket_count=sub_bucket_count,
        bucket_count=bucket_count,
        target_row_count=row_count_result.row_count,
        row_count_source=row_count_result.source.value,
    )


def _run_detection_phase(
    source: DataSource,
    spark: SparkSession,
    source_connection: SourceConnectionConfig,
    target_connection: TargetConnectionConfig,
    table_conf: Table,
    detection_cols: list[Schema],
    target_detection_cols: list[Schema],
    column_mapping: dict[str, str] | None,
    query_builder: FingerprintQueryBuilder,
    tier: TierSelection,
) -> tuple[DetectionResult, int]:
    """Run detection aggregates on both sides; return (result, elapsed_ms)."""
    start_time = time.monotonic()
    source_detection_sql = query_builder.build_detection_sql(
        schema=source_connection.schema,
        table=table_conf.source_name,
        columns=detection_cols,
        column_mapping=column_mapping,
        sub_bucket_count=tier.sub_bucket_count,
    )
    source_agg_df = source.read_data(
        catalog=source_connection.catalog,
        schema=source_connection.schema,
        table=table_conf.source_name,
        query=source_detection_sql,
        options=table_conf.jdbc_reader_options,
    )
    target_agg_df = compute_target_fingerprint(
        spark=spark,
        catalog=target_connection.catalog,
        schema=target_connection.schema,
        table=table_conf.target_name,
        columns=target_detection_cols,
        column_mapping=None,
        sub_bucket_count=tier.sub_bucket_count,
    )
    detection = detect_and_solve(source_agg_df, target_agg_df)
    elapsed_ms = int((time.monotonic() - start_time) * 1000)
    return detection, elapsed_ms


@dataclass(frozen=True)
class FetchContext:
    """Inputs the fetch phase needs."""

    source: DataSource
    target: DataSource
    source_engine: Dialect
    source_connection: SourceConnectionConfig
    target_connection: TargetConnectionConfig
    table_conf: Table
    src_schema: list[Schema]
    tgt_schema: list[Schema]
    detection_cols: list[Schema]
    target_detection_cols: list[Schema]
    column_mapping: dict[str, str] | None
    query_builder: FingerprintQueryBuilder
    tier: TierSelection


def fetch_source_rows(
    ctx: FetchContext,
    solved_hashes: dict[int, list[int]],
    unsolved_sb_ids: list[int],
    report_type: str,
) -> tuple[DataFrame, str]:
    """Fetch source rows for Stage-2 reconcile."""
    source_filter_subquery = ctx.query_builder.build_source_filter_subquery(
        schema=ctx.source_connection.schema,
        table=ctx.table_conf.source_name,
        columns=ctx.detection_cols,
        sub_bucket_count=ctx.tier.sub_bucket_count,
        solved_hashes=solved_hashes,
        unsolved_sb_ids=unsolved_sb_ids,
    )
    transformer = RuleBasedColumnTransformer(
        source=ReconcileLayer(ctx.source, ctx.source_engine, ctx.src_schema),
        target=ReconcileLayer(ctx.target, get_dialect("databricks"), ctx.tgt_schema),
        table_conf=ctx.table_conf,
    )
    src_hash_builder = HashQueryBuilder(
        ctx.table_conf, ctx.src_schema, "source", ctx.source_engine, ctx.source, transformer
    )
    src_filtered_query = src_hash_builder.build_query(
        report_type=report_type, project_all_columns=True, from_expression=source_filter_subquery
    )

    df = ctx.source.read_data(
        catalog=ctx.source_connection.catalog,
        schema=ctx.source_connection.schema,
        table=ctx.table_conf.source_name,
        query=src_filtered_query,
        options=ctx.table_conf.jdbc_reader_options,
    )
    return df, FETCH_PATH_V1_SANDWICH


def fetch_target_rows(
    ctx: FetchContext,
    solved_hashes: dict[int, list[int]],
    unsolved_sb_ids: list[int],
    report_type: str,
) -> DataFrame:
    """Fetch target rows for Stage-2 reconcile via the Spark-side filter subquery."""
    transformer = RuleBasedColumnTransformer(
        source=ReconcileLayer(ctx.source, ctx.source_engine, ctx.src_schema),
        target=ReconcileLayer(ctx.target, get_dialect("databricks"), ctx.tgt_schema),
        table_conf=ctx.table_conf,
    )
    tgt_hash_builder = HashQueryBuilder(
        ctx.table_conf, ctx.tgt_schema, "target", ctx.source_engine, ctx.target, transformer
    )
    tgt_filter_subquery = build_target_filter_subquery(
        ctx.target_connection.catalog,
        ctx.target_connection.schema,
        ctx.table_conf.target_name,
        ctx.target_detection_cols,
        None,
        solved_hashes,
        unsolved_sb_ids,
        sub_bucket_count=ctx.tier.sub_bucket_count,
    )
    tgt_filtered_query = tgt_hash_builder.build_query(
        report_type=report_type, project_all_columns=True, from_expression=tgt_filter_subquery
    )
    return ctx.target.read_data(
        catalog=ctx.target_connection.catalog,
        schema=ctx.target_connection.schema,
        table=ctx.table_conf.target_name,
        query=tgt_filtered_query,
        options=None,
    )


def fetch_source_and_target_rows(
    ctx: FetchContext,
    solved_hashes: dict[int, list[int]],
    unsolved_sb_ids: list[int],
    report_type: str,
) -> tuple[DataFrame, str, DataFrame]:
    """Run the Stage-2 source and target fetches; return ``(src_df, fetch_path, tgt_df)``."""
    src_data, fetch_path = fetch_source_rows(ctx, solved_hashes, unsolved_sb_ids, report_type)
    tgt_data = fetch_target_rows(ctx, solved_hashes, unsolved_sb_ids, report_type)
    return src_data, fetch_path, tgt_data


@dataclass(frozen=True)
class ConnectionConfigPair:
    """Source + target UC connection configs, re-paired for the pre-check entry point."""

    source: SourceConnectionConfig
    target: TargetConnectionConfig


def run_fingerprint_precheck(
    source: DataSource,
    target: DataSource,
    spark: SparkSession,
    source_engine: Dialect,
    connections: ConnectionConfigPair,
    table_conf: Table,
    src_schema: list[Schema],
    tgt_schema: list[Schema],
    report_type: str,
    data_source: str,
    recon_id: str | None = None,
) -> FingerprintResult | None:
    """Execute the fingerprint pre-check for one table pair, or None if ineligible."""
    log_tag = f"Fingerprint[recon_id={recon_id}]" if recon_id else "Fingerprint"
    alignment = align_columns(table_conf, src_schema, tgt_schema)
    if alignment is None:
        logger.info(f"{log_tag}: table '{table_conf.source_name}' ineligible — skipping pre-check")
        return None

    detection_cols = resolve_detection_columns(table_conf, src_schema, source, source_engine)
    if detection_cols is None:
        return None

    target_detection_cols = resolve_target_detection_columns(detection_cols, tgt_schema, alignment.column_mapping)
    if target_detection_cols is None:
        return None
    detection_cols, target_detection_cols = pair_detection_columns(detection_cols, target_detection_cols)

    query_builder = get_query_builder(data_source)

    tier = select_tier(spark, connections.target, table_conf)

    detection, elapsed_ms = _run_detection_phase(
        source,
        spark,
        connections.source,
        connections.target,
        table_conf,
        detection_cols,
        target_detection_cols,
        alignment.column_mapping,
        query_builder,
        tier,
    )

    if detection.verdict == "MATCH":
        return FingerprintResult(
            verdict="MATCH",
            detection_elapsed_ms=elapsed_ms,
            sub_bucket_count=tier.sub_bucket_count,
            bucket_count=tier.bucket_count,
            target_row_count=tier.target_row_count,
            row_count_source=tier.row_count_source,
        )

    if detection.systemic_mismatch:
        logger.info(f"{log_tag}: systemic mismatch — deferring to full pipeline")
        return None

    fetch_ctx = FetchContext(
        source=source,
        target=target,
        source_engine=source_engine,
        source_connection=connections.source,
        target_connection=connections.target,
        table_conf=table_conf,
        src_schema=src_schema,
        tgt_schema=tgt_schema,
        detection_cols=detection_cols,
        target_detection_cols=target_detection_cols,
        column_mapping=alignment.column_mapping,
        query_builder=query_builder,
        tier=tier,
    )
    return _build_mismatch_result(fetch_ctx, detection, report_type, elapsed_ms)


def _build_mismatch_result(
    ctx: FetchContext,
    detection: DetectionResult,
    report_type: str,
    detection_elapsed_ms: int,
) -> FingerprintResult | None:
    """Fetch the culprit rows for a MISMATCH detection and assemble the result."""
    solved_hashes = collect_solved_hashes(detection)
    unsolved_sb_ids = detection.unsolved_sb_ids
    if not solved_hashes and not unsolved_sb_ids:
        return None

    src_data, fetch_path, tgt_data = fetch_source_and_target_rows(ctx, solved_hashes, unsolved_sb_ids, report_type)

    tier = ctx.tier
    return FingerprintResult(
        verdict="MISMATCH",
        source_rows=src_data,
        target_rows=tgt_data,
        solved_count=len(detection.solved_results),
        unsolved_sb_count=len(detection.unsolved_sb_ids),
        total_mismatched_sbs=detection.total_mismatched_sbs,
        detection_elapsed_ms=detection_elapsed_ms,
        sub_bucket_count=tier.sub_bucket_count,
        bucket_count=tier.bucket_count,
        target_row_count=tier.target_row_count,
        row_count_source=tier.row_count_source,
        fetch_path=fetch_path,
    )


_QUERY_BUILDERS: dict[str, type[FingerprintQueryBuilder]] = {
    "redshift": RedshiftFingerprintQueryBuilder,
}


def get_query_builder(data_source: str) -> FingerprintQueryBuilder:
    """Return the registered builder for ``data_source``."""
    try:
        builder_cls = _QUERY_BUILDERS[data_source]
    except KeyError as e:
        raise UnsupportedDataSourceError(
            f"No fingerprint query builder registered for data_source={data_source!r}. "
            f"Supported: {sorted(_QUERY_BUILDERS)}"
        ) from e
    return builder_cls()


def fingerprint_supported_sources() -> frozenset[str]:
    """Sources with a registered FingerprintQueryBuilder."""
    return frozenset(_QUERY_BUILDERS)


def collect_solved_hashes(detection: DetectionResult) -> dict[int, list[int]]:
    """Merge solved source and target hashes per sub-bucket into a single lookup."""
    accum: dict[int, set[int]] = {}
    for solve in detection.solved_results:
        if not solve.source_hashes and not solve.target_hashes:
            continue
        bucket = accum.setdefault(solve.sub_bucket_id, set())
        bucket.update(solve.source_hashes)
        bucket.update(solve.target_hashes)
    return {sb_id: sorted(hashes) for sb_id, hashes in accum.items()}
