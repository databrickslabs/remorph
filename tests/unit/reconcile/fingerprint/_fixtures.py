"""Shared test fixtures for fingerprint unit tests."""

from __future__ import annotations

from unittest.mock import MagicMock

from databricks.labs.lakebridge.config import SourceConnectionConfig, TargetConnectionConfig
from databricks.labs.lakebridge.reconcile.fingerprint.orchestrator import (
    FetchContext,
    TierSelection,
)
from databricks.labs.lakebridge.reconcile.fingerprint.row_count import RowCountSource
from databricks.labs.lakebridge.reconcile.recon_config import Schema, Table

FP_METRICS_FIELD_ORDER = (
    "eligible",
    "ineligibility_reason",
    "verdict",
    "elapsed_ms",
    "solved_count",
    "unsolved_sb_count",
    "total_mismatched_sbs",
    "fallback_to_full_pipeline",
    "sub_bucket_count",
    "bucket_count",
    "target_row_count",
    "row_count_source",
    "fetch_path",
)


def make_source_connection(
    *,
    dialect: str = "redshift",
    catalog: str = "source_catalog",
    schema: str = "public",
    uc_connection_name: str | None = "test_connection",
) -> SourceConnectionConfig:
    return SourceConnectionConfig(
        dialect=dialect,
        catalog=catalog,
        schema=schema,
        uc_connection_name=uc_connection_name,
    )


def make_target_connection(
    *,
    catalog: str = "test_catalog",
    schema: str = "perf_test",
) -> TargetConnectionConfig:
    return TargetConnectionConfig(catalog=catalog, schema=schema)


def make_table_conf(
    *,
    source_name: str = "orders",
    target_name: str = "orders",
    join_columns: list[str] | None = None,
    jdbc_reader_options=None,
) -> Table:
    return Table(
        source_name=source_name,
        target_name=target_name,
        join_columns=list(join_columns) if join_columns is not None else ["order_id"],
        jdbc_reader_options=jdbc_reader_options,
    )


def make_schema() -> list[Schema]:
    return [
        Schema("`order_id`", "bigint", '"order_id"'),
        Schema("`order_amount`", "numeric(10,2)", '"order_amount"'),
    ]


def make_tier(
    *,
    sub_bucket_count: int = 2_097_152,
    bucket_count: int = 2_048,
    target_row_count: int = 100_000_000,
    row_count_source: str = RowCountSource.DELTA_DESCRIBE_DETAIL.value,
) -> TierSelection:
    return TierSelection(
        sub_bucket_count=sub_bucket_count,
        bucket_count=bucket_count,
        target_row_count=target_row_count,
        row_count_source=row_count_source,
    )


def make_fetch_ctx(
    *,
    source: MagicMock | None = None,
    target: MagicMock | None = None,
    query_builder: MagicMock | None = None,
) -> FetchContext:
    return FetchContext(
        source=source if source is not None else MagicMock(),
        target=target if target is not None else MagicMock(),
        source_engine=MagicMock(),
        source_connection=make_source_connection(),
        target_connection=make_target_connection(),
        table_conf=make_table_conf(),
        src_schema=make_schema(),
        tgt_schema=make_schema(),
        detection_cols=make_schema(),
        target_detection_cols=make_schema(),
        column_mapping=None,
        query_builder=query_builder if query_builder is not None else MagicMock(),
        tier=make_tier(),
    )


def make_fake_hash_builder(hash_query: str) -> MagicMock:
    fake = MagicMock()

    def _build_query(report_type, *, project_all_columns=False, from_expression=None):
        del report_type, project_all_columns
        if from_expression is None:
            return hash_query
        spliced = hash_query
        for placeholder in (":tbl", "%(tbl)s"):
            spliced = spliced.replace(placeholder, from_expression)
        return spliced

    fake.build_query.side_effect = _build_query
    return fake


def assert_project_all_columns_kwargs(call_kwargs: dict, *, side: str) -> None:
    assert call_kwargs.get("report_type") == "data"
    assert call_kwargs.get("project_all_columns") is True, (
        f"Fingerprint Stage-2 {side}-fetch must request all-columns projection so "
        f"compare.capture_mismatch_data_and_columns can populate mismatch_columns. "
        f"Got kwargs={call_kwargs!r}"
    )


def make_describe_detail_df(num_records: int | None) -> MagicMock:
    df = MagicMock()
    df.columns = ["numRecords"]
    select_result = MagicMock()
    if num_records is None:
        select_result.collect.return_value = []
    else:
        row = MagicMock()
        row.__getitem__.side_effect = lambda key: {"numRecords": num_records}[key]
        select_result.collect.return_value = [row]
    df.select.return_value = select_result
    return df
