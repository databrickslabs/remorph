"""Unit tests for orchestrator-level adaptive sub-bucket tier selection."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from pyspark.sql.utils import AnalysisException

from databricks.labs.lakebridge.reconcile.fingerprint import orchestrator as orch
from databricks.labs.lakebridge.reconcile.fingerprint.constants import (
    BUCKET_COUNT,
    SUB_BUCKET_COUNT,
)
from databricks.labs.lakebridge.reconcile.fingerprint.engine import DetectionResult
from databricks.labs.lakebridge.reconcile.fingerprint.orchestrator import (
    ColumnAlignment,
    select_tier,
)
from databricks.labs.lakebridge.reconcile.fingerprint.row_count import RowCountSource
from databricks.labs.lakebridge.reconcile.recon_config import Schema
from tests.unit.reconcile.fingerprint._fixtures import (
    make_describe_detail_df,
    make_source_connection,
    make_table_conf,
    make_target_connection,
)


@pytest.mark.parametrize(
    ("num_records", "expected_sub_buckets", "expected_buckets", "expected_source"),
    [
        (10_000, 16_384, 128, RowCountSource.DELTA_DESCRIBE_DETAIL),
        (10_000_000, 1_048_576, 1_024, RowCountSource.DELTA_DESCRIBE_DETAIL),
        (100_000_000, 2_097_152, 2_048, RowCountSource.DELTA_DESCRIBE_DETAIL),
        (1_000_000_000, 4_194_304, 4_096, RowCountSource.DELTA_DESCRIBE_DETAIL),
        (20_000_000_000, 8_388_608, 8_192, RowCountSource.DELTA_DESCRIBE_DETAIL),
        (100_000_000_000, 16_777_216, 16_384, RowCountSource.DELTA_DESCRIBE_DETAIL),
    ],
)
def test_select_tier_picks_correct_tier_from_target_delta_count(
    num_records, expected_sub_buckets, expected_buckets, expected_source
):
    spark = MagicMock()
    spark.sql.return_value = make_describe_detail_df(num_records)
    tier = select_tier(spark, make_target_connection(), make_table_conf())
    assert tier.sub_bucket_count == expected_sub_buckets
    assert tier.bucket_count == expected_buckets
    assert tier.target_row_count == num_records
    assert tier.row_count_source == expected_source.value


def test_select_tier_falls_back_to_static_default_when_describe_detail_fails():
    spark = MagicMock()
    spark.sql.side_effect = AnalysisException("Table or view not found: test_catalog.perf_test.orders")
    tier = select_tier(spark, make_target_connection(), make_table_conf())
    assert tier.sub_bucket_count == SUB_BUCKET_COUNT
    assert tier.bucket_count == BUCKET_COUNT
    assert tier.target_row_count is None
    assert tier.row_count_source == RowCountSource.STATIC_DEFAULT.value


def test_select_tier_uses_count_star_when_describe_detail_lacks_num_records():
    describe = MagicMock()
    describe.columns = ["format", "numFiles", "sizeInBytes"]

    count_df = MagicMock()
    count_row = MagicMock()
    count_row.__getitem__.side_effect = lambda k: {"cnt": 1_000_000}[k]
    count_df.collect.return_value = [count_row]

    spark = MagicMock()
    spark.sql.side_effect = lambda query, *a, **k: count_df if "COUNT(*)" in query else describe

    tier = select_tier(spark, make_target_connection(), make_table_conf())
    assert tier.target_row_count == 1_000_000
    assert tier.row_count_source == RowCountSource.COUNT_STAR.value
    assert tier.sub_bucket_count == 1_048_576
    assert tier.bucket_count == 1_024


def test_select_tier_uses_target_catalog_and_schema_not_source():
    spark = MagicMock()
    spark.sql.return_value = make_describe_detail_df(100_000_000)
    select_tier(spark, make_target_connection(), make_table_conf(target_name="my_target_table"))
    spark.sql.assert_called_once()
    call_arg = spark.sql.call_args[0][0]
    assert (
        "`test_catalog`.`perf_test`.`my_target_table`" in call_arg
    ), f"select_tier must DESCRIBE DETAIL the TARGET table; got SQL: {call_arg!r}"
    assert "source_catalog" not in call_arg, (
        f"select_tier must NEVER reference source catalog (Redshift side has no Delta metadata); "
        f"got SQL: {call_arg!r}"
    )


def test_run_fingerprint_precheck_passes_same_tier_to_source_and_target():
    captured_tier_detection: list = []

    fake_detection = DetectionResult(verdict="MATCH")

    def fake_detection_phase(*args, **kwargs):
        tier = kwargs.get("tier") if "tier" in kwargs else args[-1]
        captured_tier_detection.append(tier)
        return fake_detection, 42

    def fake_resolve_cols(*_args, **_kwargs):
        return [Schema("`order_id`", "bigint", '"order_id"')]

    def fake_align_columns(*_args, **_kwargs):
        return ColumnAlignment(column_mapping=None)

    spark = MagicMock()
    spark.sql.return_value = make_describe_detail_df(100_000_000)
    source = MagicMock()
    target = MagicMock()
    source_engine = MagicMock()

    with (
        patch.object(orch, "_run_detection_phase", side_effect=fake_detection_phase),
        patch.object(orch, "resolve_detection_columns", side_effect=fake_resolve_cols),
        patch.object(orch, "resolve_target_detection_columns", side_effect=fake_resolve_cols),
        patch.object(orch, "align_columns", side_effect=fake_align_columns),
        patch.object(orch, "get_query_builder", return_value=MagicMock()),
    ):
        result = orch.run_fingerprint_precheck(
            source=source,
            target=target,
            spark=spark,
            source_engine=source_engine,
            connections=orch.ConnectionConfigPair(source=make_source_connection(), target=make_target_connection()),
            table_conf=make_table_conf(),
            src_schema=[],
            tgt_schema=[],
            report_type="data",
            data_source="redshift",
        )

    assert len(captured_tier_detection) == 1
    tier = captured_tier_detection[0]
    assert tier.sub_bucket_count == 2_097_152
    assert tier.bucket_count == 2_048

    assert result is not None
    assert result.verdict == "MATCH"
    assert result.sub_bucket_count == 2_097_152
    assert result.bucket_count == 2_048
    assert result.target_row_count == 100_000_000
    assert result.row_count_source == "delta_describe_detail"


def test_fingerprint_result_carries_static_default_provenance_on_describe_detail_failure():
    fake_detection = DetectionResult(verdict="MATCH")

    def fake_detection_phase(*_args, **_kwargs):
        return fake_detection, 42

    def fake_resolve_cols(*_args, **_kwargs):
        return [Schema("`order_id`", "bigint", '"order_id"')]

    def fake_align_columns(*_args, **_kwargs):
        return ColumnAlignment(column_mapping=None)

    spark = MagicMock()
    spark.sql.side_effect = AnalysisException("table not found")
    source = MagicMock()
    target = MagicMock()
    source_engine = MagicMock()

    with (
        patch.object(orch, "_run_detection_phase", side_effect=fake_detection_phase),
        patch.object(orch, "resolve_detection_columns", side_effect=fake_resolve_cols),
        patch.object(orch, "resolve_target_detection_columns", side_effect=fake_resolve_cols),
        patch.object(orch, "align_columns", side_effect=fake_align_columns),
        patch.object(orch, "get_query_builder", return_value=MagicMock()),
    ):
        result = orch.run_fingerprint_precheck(
            source=source,
            target=target,
            spark=spark,
            source_engine=source_engine,
            connections=orch.ConnectionConfigPair(source=make_source_connection(), target=make_target_connection()),
            table_conf=make_table_conf(),
            src_schema=[],
            tgt_schema=[],
            report_type="data",
            data_source="redshift",
        )

    assert result is not None
    assert result.verdict == "MATCH"
    assert result.sub_bucket_count == SUB_BUCKET_COUNT
    assert result.bucket_count == BUCKET_COUNT
    assert result.target_row_count is None
    assert result.row_count_source == "static_default"
