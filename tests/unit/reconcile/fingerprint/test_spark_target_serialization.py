"""Pin fingerprint target serialisation to the shared row-hash transform map."""

from __future__ import annotations

import pytest

from databricks.labs.lakebridge.reconcile.fingerprint.columns import DetectionColumn
from databricks.labs.lakebridge.reconcile.fingerprint.spark_target import (
    build_target_filter_subquery,
    quote_spark_identifier,
    serialize_target_column_sql,
)
from databricks.labs.lakebridge.reconcile.query_builder.column_transformer import serialize_column_for_hash
from databricks.labs.lakebridge.reconcile.recon_config import Schema


@pytest.mark.parametrize(
    "col_type, counterpart_type, expected",
    [
        ("string", None, "COALESCE(TRIM(`notes`), '_null_recon_')"),
        ("int", None, "COALESCE(TRIM(`notes`), '_null_recon_')"),
        ("timestamp", "timestamp", "COALESCE(DATE_FORMAT(`notes`, 'yyyy-MM-dd HH:mm:ss.SSSSSS'), '_null_recon_')"),
        ("date", None, "COALESCE(TRIM(`notes`), '_null_recon_')"),
        (
            "double",
            "double precision",
            "COALESCE(CASE WHEN ISNAN(`notes`) OR `notes` IN (CAST('Infinity' AS DOUBLE), "
            "CAST('-Infinity' AS DOUBLE)) OR ABS(`notes`) >= 1e28 THEN CAST(`notes` AS STRING) "
            "ELSE CAST(CAST(`notes` AS DECIMAL(38,10)) AS STRING) END, '_null_recon_')",
        ),
    ],
)
def test_target_serializer_matches_shared_transform_map(
    col_type: str, counterpart_type: str | None, expected: str
) -> None:
    sql = serialize_target_column_sql("notes", col_type, counterpart_type)
    assert sql == expected
    assert sql == serialize_column_for_hash("`notes`", col_type, counterpart_type, "target")


@pytest.mark.parametrize("col_type", ["timestamp", "timestamptz", "timestamp with time zone"])
def test_target_timestamp_renders_plain_date_format_and_matches_rowhash(col_type: str) -> None:
    sql = serialize_target_column_sql("event_ts", col_type, "timestamp")
    assert "CONVERT_TIMEZONE" not in sql, sql
    assert "TO_UTC_TIMESTAMP" not in sql, sql
    assert "DATE_FORMAT(`event_ts`, 'yyyy-MM-dd HH:mm:ss.SSSSSS')" in sql, sql
    assert sql == serialize_column_for_hash("`event_ts`", col_type, "timestamp", "target")


def test_build_target_filter_subquery_serialises_via_transform_map() -> None:
    columns = [
        Schema("`order_id`", "int", "`order_id`"),
        Schema("`notes`", "varchar(64)", "`notes`"),
    ]
    sql = build_target_filter_subquery(
        catalog="test_catalog",
        schema="fp_correctness",
        table="orders",
        columns=columns,
        column_mapping=None,
        solved_hashes={1: [101, 102]},
        unsolved_sb_ids=[7],
        sub_bucket_count=1024,
    )
    assert "COALESCE(TRIM(`order_id`), '_null_recon_')" in sql, sql
    assert "COALESCE(TRIM(`notes`), '_null_recon_')" in sql, sql
    assert "FROM `test_catalog`.`fp_correctness`.`orders`" in sql, sql
    assert "_fp_filtered" in sql


def test_build_target_filter_subquery_omits_catalog_when_unset() -> None:
    sql = build_target_filter_subquery(
        catalog=None,
        schema="schema_only",
        table="orders",
        columns=[Schema("`order_id`", "int", "`order_id`")],
        column_mapping=None,
        solved_hashes={},
        unsolved_sb_ids=[1, 2],
        sub_bucket_count=1024,
    )
    assert "FROM `schema_only`.`orders`" in sql, sql
    assert "test_catalog." not in sql


def test_build_target_filter_subquery_uses_date_format_for_timestamps() -> None:
    columns = [
        Schema("`order_id`", "int", "`order_id`"),
        DetectionColumn("`event_ts`", "timestamp", "`event_ts`", "timestamp"),
    ]
    sql = build_target_filter_subquery(
        catalog="c",
        schema="s",
        table="t",
        columns=columns,
        column_mapping=None,
        solved_hashes={1: [101]},
        unsolved_sb_ids=[],
        sub_bucket_count=1024,
    )
    assert "DATE_FORMAT(`event_ts`, 'yyyy-MM-dd HH:mm:ss.SSSSSS')" in sql, sql
    assert "TO_UTC_TIMESTAMP" not in sql, sql
    assert "COALESCE(TRIM(`order_id`), '_null_recon_')" in sql, sql


def test_build_target_filter_subquery_resolves_column_mapping() -> None:
    sql = build_target_filter_subquery(
        catalog="c",
        schema="s",
        table="t",
        columns=[Schema("`src_id`", "int", "`src_id`")],
        column_mapping={"src_id": "tgt_id"},
        solved_hashes={0: [1]},
        unsolved_sb_ids=[],
        sub_bucket_count=1024,
    )
    assert "`tgt_id`" in sql, sql
    assert "`src_id`" not in sql, sql


def test_serialize_target_column_handles_dot_in_column_name() -> None:
    sql = serialize_target_column_sql("a.b", "string")
    assert "`a.b`" in sql, sql


def test_quote_spark_identifier_doubles_embedded_backtick() -> None:
    assert quote_spark_identifier("plain") == "`plain`"
    assert quote_spark_identifier("we`ird") == "`we``ird`"
    assert quote_spark_identifier("``") == "``````"


def test_quote_spark_identifier_handles_dot() -> None:
    assert quote_spark_identifier("a.b") == "`a.b`"
    assert quote_spark_identifier("event.timestamp.utc") == "`event.timestamp.utc`"
