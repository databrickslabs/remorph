"""Unit tests for fingerprint orchestrator helpers."""

from unittest.mock import MagicMock, create_autospec

import pytest
from pyspark.sql.types import DecimalType

from databricks.labs.lakebridge.reconcile.connectors.data_source import DataSource
from databricks.labs.lakebridge.reconcile.connectors.dialect_utils import DialectUtils
from databricks.labs.lakebridge.reconcile.fingerprint import orchestrator, spark_target
from databricks.labs.lakebridge.reconcile.fingerprint.engine import DetectionResult, SolveResult
from databricks.labs.lakebridge.reconcile.fingerprint.exceptions import UnmappedTargetColumnMappingError
from databricks.labs.lakebridge.reconcile.fingerprint.orchestrator import (
    align_columns,
    collect_solved_hashes,
    fingerprint_supported_sources,
    get_query_builder,
    resolve_detection_columns,
    resolve_target_detection_columns,
)
from databricks.labs.lakebridge.reconcile.fingerprint.query_builders.redshift import (
    RedshiftFingerprintQueryBuilder,
)
from databricks.labs.lakebridge.reconcile.recon_config import ColumnMapping, Schema, Table
from databricks.labs.lakebridge.reconcile.recon_output_config import DataReconcileOutput, MismatchOutput
from databricks.labs.lakebridge.transpiler.sqlglot.dialect_utils import get_dialect


def test_collect_solved_hashes_merges_same_sub_bucket():
    detection = DetectionResult(
        verdict="MISMATCH",
        solved_results=[
            SolveResult(sub_bucket_id=7, source_hashes=[100], target_hashes=[]),
            SolveResult(sub_bucket_id=7, source_hashes=[], target_hashes=[200]),
        ],
    )
    out = collect_solved_hashes(detection)
    assert out[7] == [100, 200]


def test_collect_solved_hashes_dedupes_within_and_across_solves():
    detection = DetectionResult(
        verdict="MISMATCH",
        solved_results=[
            SolveResult(sub_bucket_id=7, source_hashes=[100, 200], target_hashes=[100]),
            SolveResult(sub_bucket_id=7, source_hashes=[100, 300], target_hashes=[]),
        ],
    )
    out = collect_solved_hashes(detection)
    assert out[7] == [100, 200, 300]


def test_align_columns_rejects_unmapped_target_column():
    table_conf = Table(
        source_name="orders",
        target_name="orders",
        join_columns=["order_id"],
        column_mapping=[ColumnMapping(source_name="src_a", target_name="tgt_a_typo")],
    )
    src_schema = [
        Schema("`src_a`", "int", '"src_a"'),
        Schema("`order_id`", "bigint", '"order_id"'),
    ]
    tgt_schema = [
        Schema("`tgt_a`", "int", "`tgt_a`"),
        Schema("`order_id`", "bigint", "`order_id`"),
    ]
    with pytest.raises(UnmappedTargetColumnMappingError, match="tgt_a_typo"):
        align_columns(table_conf, src_schema, tgt_schema)


def test_align_columns_accepts_validated_target_column_mapping():
    table_conf = Table(
        source_name="orders",
        target_name="orders",
        join_columns=["order_id"],
        column_mapping=[ColumnMapping(source_name="src_a", target_name="tgt_a")],
    )
    src_schema = [
        Schema("`src_a`", "int", '"src_a"'),
        Schema("`order_id`", "bigint", '"order_id"'),
    ]
    tgt_schema = [
        Schema("`tgt_a`", "int", "`tgt_a`"),
        Schema("`order_id`", "bigint", "`order_id`"),
    ]
    alignment = align_columns(table_conf, src_schema, tgt_schema)
    assert alignment is not None
    assert alignment.column_mapping == {"src_a": "tgt_a"}


def test_column_mapping_lookup_is_case_insensitive():
    table_conf = Table(
        source_name="orders",
        target_name="orders",
        join_columns=["order_id"],
        column_mapping=[ColumnMapping(source_name="CustId", target_name="customer_id")],
    )
    src_schema = [
        Schema("`custid`", "int", '"custid"'),
        Schema("`order_id`", "bigint", '"order_id"'),
    ]
    tgt_schema = [
        Schema("`customer_id`", "int", "`customer_id`"),
        Schema("`order_id`", "bigint", "`order_id`"),
    ]
    alignment = align_columns(table_conf, src_schema, tgt_schema)
    assert alignment is not None
    assert alignment.column_mapping == {"custid": "customer_id"}
    target_cols = resolve_target_detection_columns(src_schema, tgt_schema, alignment.column_mapping)
    assert target_cols is not None
    subquery = spark_target.build_target_filter_subquery(
        None,
        "sch",
        "orders",
        target_cols,
        None,
        solved_hashes={},
        unsolved_sb_ids=[0],
        sub_bucket_count=64,
    )
    assert "`customer_id`" in subquery
    assert "`custid`" not in subquery
    assert "`order_id`" in subquery


def test_column_mapping_target_is_not_double_delimited_after_normalization():
    table_conf = Table(
        source_name="`orders`",
        target_name="`orders`",
        join_columns=["order_id"],
        column_mapping=[ColumnMapping(source_name="`src_a`", target_name="`customer_id`")],
    )
    src_schema = [
        Schema("`src_a`", "int", '"src_a"'),
        Schema("`order_id`", "bigint", '"order_id"'),
    ]
    tgt_schema = [
        Schema("`customer_id`", "int", "`customer_id`"),
        Schema("`order_id`", "bigint", "`order_id`"),
    ]
    alignment = align_columns(table_conf, src_schema, tgt_schema)
    assert alignment is not None
    assert alignment.column_mapping == {"src_a": "customer_id"}

    target_cols = resolve_target_detection_columns(src_schema, tgt_schema, alignment.column_mapping)
    assert target_cols is not None
    subquery = spark_target.build_target_filter_subquery(
        None,
        "sch",
        "orders",
        target_cols,
        None,
        solved_hashes={},
        unsolved_sb_ids=[0],
        sub_bucket_count=64,
    )
    assert "`customer_id`" in subquery
    assert "``" not in subquery


def test_target_detection_uses_target_column_type_not_source_type():
    src_detection_cols = [Schema("`amount`", "double", '"amount"')]
    tgt_schema = [Schema("`amount`", "decimal(18,2)", "`amount`")]

    target_cols = resolve_target_detection_columns(src_detection_cols, tgt_schema, None)
    assert target_cols is not None
    assert target_cols[0].data_type == "decimal(18,2)"

    subquery = spark_target.build_target_filter_subquery(
        None,
        "sch",
        "orders",
        target_cols,
        None,
        solved_hashes={},
        unsolved_sb_ids=[0],
        sub_bucket_count=64,
    )
    assert "ISNAN" not in subquery.upper(), subquery
    assert "38, 10" not in subquery and "38,10" not in subquery, subquery


def test_resolve_target_detection_columns_declines_when_target_missing():
    src_detection_cols = [Schema("`ghost`", "int", '"ghost"')]
    tgt_schema = [Schema("`order_id`", "bigint", "`order_id`")]
    assert resolve_target_detection_columns(src_detection_cols, tgt_schema, None) is None


def test_query_builder_registry_returns_redshift_builder():
    builder = get_query_builder("redshift")
    assert isinstance(builder, RedshiftFingerprintQueryBuilder)


def test_query_builder_does_not_collapse_empty_to_null():
    builder = get_query_builder("redshift")
    serialized = builder.serialize_column("`notes`", "VARCHAR")
    assert "NULLIF" not in serialized
    assert serialized == 'COALESCE(TRIM("notes"), \'_null_recon_\')'


def test_query_builder_registry_rejects_unknown_source():
    with pytest.raises(ValueError, match="No fingerprint query builder registered"):
        get_query_builder("mysql")


def test_fingerprint_supported_sources_contains_redshift():
    supported = fingerprint_supported_sources()
    assert "redshift" in supported
    for source in supported:
        assert get_query_builder(source) is not None


def test_resolve_detection_columns_strips_identifier_delimiters():
    src_schema = [
        Schema("`color`", "varchar(2)", '"color"'),
        Schema("`clarity`", "varchar(5)", '"clarity"'),
        Schema("`carat`", "decimal(5,2)", '"carat"'),
    ]
    table_conf = Table(
        source_name="diamonds",
        target_name="diamonds",
        join_columns=["color", "clarity"],
        select_columns=["color", "clarity"],
    )
    source = create_autospec(DataSource, instance=True)
    source.normalize_identifier.side_effect = lambda ident: type(
        "NI", (), {"ansi_normalized": f"`{ident}`", "source_normalized": f'"{ident}"'}
    )()

    resolved = resolve_detection_columns(table_conf, src_schema, source, get_dialect("redshift"))

    assert resolved is not None
    resolved_names = [_strip_delim(s.ansi_normalized_column_name) for s in resolved]
    assert sorted(resolved_names) == ["clarity", "color"]


def _strip_delim(name: str) -> str:
    return DialectUtils.unnormalize_identifier(name)


def test_build_mismatch_output_backfills_mismatch_columns_for_report_all(monkeypatch):
    captured_calls: dict = {}

    fake_skinny_mismatch_df = object()
    fake_wide_capture_df = object()

    def fake_compare_reconcile_data(*, source, target, key_columns, report_type, persistence, max_sample_size):
        del persistence
        captured_calls["compare_reconcile_data"] = {
            "source": source,
            "target": target,
            "key_columns": key_columns,
            "report_type": report_type,
            "max_sample_size": max_sample_size,
        }
        return DataReconcileOutput(
            mismatch_count=3,
            missing_in_src_count=0,
            missing_in_tgt_count=0,
            mismatch=MismatchOutput(mismatch_df=fake_skinny_mismatch_df, mismatch_columns=None),
        )

    def fake_capture_mismatch_data_and_columns(*, source, target, key_columns, persistence, sample_size):
        del persistence
        captured_calls["capture_mismatch_data_and_columns"] = {
            "source_columns": list(source.columns),
            "target_columns": list(target.columns),
            "key_columns": key_columns,
            "sample_size": sample_size,
        }
        return MismatchOutput(mismatch_df=fake_wide_capture_df, mismatch_columns=["s_name", "s_acctbal"])

    monkeypatch.setattr(orchestrator, "compare_reconcile_data", fake_compare_reconcile_data)
    monkeypatch.setattr(orchestrator, "capture_mismatch_data_and_columns", fake_capture_mismatch_data_and_columns)

    cache_events = {"cached": 0, "unpersisted": 0}

    class FakeDF:
        def __init__(self, cols):
            self.columns = list(cols)

        def drop(self, name):
            return FakeDF([c for c in self.columns if c != name])

        def select(self, *cols):
            return FakeDF(list(cols))

        def cache(self):
            cache_events["cached"] += 1
            return self

        def unpersist(self, blocking=False):
            del blocking
            cache_events["unpersisted"] += 1
            return self

    src = FakeDF(["s_suppkey", "s_nationkey", "s_name", "s_acctbal", "hash_value_recon"])
    tgt = FakeDF(["s_suppkey", "s_nationkey", "s_name", "s_acctbal", "hash_value_recon"])

    out = orchestrator.build_mismatch_output(
        src_hashed=src,
        tgt_hashed=tgt,
        key_columns=["s_suppkey", "s_nationkey"],
        report_type="all",
        persistence=MagicMock(is_serverless=False),
        max_sample_size=50,
    )

    assert out.mismatch.mismatch_columns == ["s_name", "s_acctbal"]
    assert cache_events["cached"] == 2
    assert cache_events["unpersisted"] == 2
    assert out.mismatch.mismatch_df is fake_wide_capture_df
    assert out.mismatch.mismatch_df is not fake_skinny_mismatch_df
    assert out.mismatch_count == 3
    assert captured_calls["capture_mismatch_data_and_columns"]["sample_size"] == 50
    assert captured_calls["compare_reconcile_data"]["max_sample_size"] == 50
    assert "hash_value_recon" not in captured_calls["capture_mismatch_data_and_columns"]["source_columns"]
    assert "hash_value_recon" not in captured_calls["capture_mismatch_data_and_columns"]["target_columns"]


def test_build_mismatch_output_aligns_columns_when_source_carries_partition_column(monkeypatch):
    captured: dict = {}

    def fake_compare_reconcile_data(*, source, target, key_columns, report_type, persistence, max_sample_size):
        del source, target, key_columns, report_type, persistence, max_sample_size
        return DataReconcileOutput(
            mismatch_count=2,
            mismatch=MismatchOutput(mismatch_df=object(), mismatch_columns=None),
        )

    def fake_capture(*, source, target, key_columns, persistence, sample_size):
        del key_columns, persistence, sample_size
        captured["source_columns"] = list(source.columns)
        captured["target_columns"] = list(target.columns)
        return MismatchOutput(mismatch_df=object(), mismatch_columns=["c_val"])

    monkeypatch.setattr(orchestrator, "compare_reconcile_data", fake_compare_reconcile_data)
    monkeypatch.setattr(orchestrator, "capture_mismatch_data_and_columns", fake_capture)

    class FakeDF:
        def __init__(self, cols):
            self.columns = list(cols)

        def drop(self, name):
            return FakeDF([c for c in self.columns if c != name])

        def select(self, *cols):
            return FakeDF(list(cols))

        def cache(self):
            return self

        def unpersist(self, blocking=False):
            del blocking
            return self

    src = FakeDF(["c_key", "c_val", "c_part", "hash_value_recon"])
    tgt = FakeDF(["c_key", "c_val", "hash_value_recon"])

    out = orchestrator.build_mismatch_output(
        src_hashed=src,
        tgt_hashed=tgt,
        key_columns=["c_key"],
        report_type="all",
        persistence=MagicMock(is_serverless=False),
    )

    assert captured["source_columns"] == captured["target_columns"]
    assert set(captured["source_columns"]) == {"c_key", "c_val"}
    assert "c_part" not in captured["source_columns"]
    assert "hash_value_recon" not in captured["source_columns"]
    assert out.mismatch_count == 2


def test_build_mismatch_output_backfills_mismatch_columns_for_report_data(monkeypatch):
    fake_skinny_mismatch_df = object()
    fake_wide_capture_df = object()
    capture_call_count = {"n": 0}

    def fake_compare_reconcile_data(*, source, target, key_columns, report_type, persistence, max_sample_size):
        del source, target, key_columns, report_type, persistence, max_sample_size
        return DataReconcileOutput(
            mismatch_count=3,
            missing_in_src_count=0,
            missing_in_tgt_count=0,
            mismatch=MismatchOutput(mismatch_df=fake_skinny_mismatch_df, mismatch_columns=None),
        )

    def fake_capture(*, source, target, key_columns, persistence, sample_size):
        del source, target, key_columns, persistence, sample_size
        capture_call_count["n"] += 1
        return MismatchOutput(mismatch_df=fake_wide_capture_df, mismatch_columns=["s_name", "s_acctbal"])

    monkeypatch.setattr(orchestrator, "compare_reconcile_data", fake_compare_reconcile_data)
    monkeypatch.setattr(orchestrator, "capture_mismatch_data_and_columns", fake_capture)

    cache_events = {"cached": 0, "unpersisted": 0}

    class FakeDF:
        def __init__(self, cols):
            self.columns = list(cols)

        def drop(self, name):
            return FakeDF([c for c in self.columns if c != name])

        def select(self, *cols):
            return FakeDF(list(cols))

        def cache(self):
            cache_events["cached"] += 1
            return self

        def unpersist(self, blocking=False):
            del blocking
            cache_events["unpersisted"] += 1
            return self

    src = FakeDF(["s_suppkey", "s_name", "s_acctbal", "hash_value_recon"])
    tgt = FakeDF(["s_suppkey", "s_name", "s_acctbal", "hash_value_recon"])

    out = orchestrator.build_mismatch_output(
        src_hashed=src,
        tgt_hashed=tgt,
        key_columns=["s_suppkey"],
        report_type="data",
        persistence=MagicMock(is_serverless=False),
        max_sample_size=50,
    )

    assert capture_call_count["n"] == 1
    assert out.mismatch.mismatch_columns == ["s_name", "s_acctbal"]
    assert out.mismatch.mismatch_df is fake_wide_capture_df
    assert out.mismatch_count == 3
    assert cache_events["cached"] == 2
    assert cache_events["unpersisted"] == 2


def test_build_mismatch_output_skips_capture_when_no_mismatches(monkeypatch):
    capture_call_count = {"n": 0}

    def fake_compare_reconcile_data(*_args, **_kwargs):
        return DataReconcileOutput(mismatch_count=0, mismatch=MismatchOutput())

    def fake_capture(*_args, **_kwargs):
        capture_call_count["n"] += 1
        return MismatchOutput()

    monkeypatch.setattr(orchestrator, "compare_reconcile_data", fake_compare_reconcile_data)
    monkeypatch.setattr(orchestrator, "capture_mismatch_data_and_columns", fake_capture)

    out = orchestrator.build_mismatch_output(
        src_hashed=MagicMock(),
        tgt_hashed=MagicMock(),
        key_columns=["k"],
        report_type="all",
        persistence=MagicMock(is_serverless=False),
    )

    assert capture_call_count["n"] == 0
    assert out.mismatch_count == 0


def test_spark_target_uses_decimal_precision_for_hash_aggregates():
    assert spark_target.RH_OPERAND_TYPE == DecimalType(19, 0)
    assert spark_target.AGG_TYPE == DecimalType(38, 0)
