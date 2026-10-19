"""Golden-SQL snapshot tests for the Redshift fingerprint query builder."""

from databricks.labs.lakebridge.reconcile.fingerprint.query_builders.redshift import (
    RedshiftFingerprintQueryBuilder,
)
from databricks.labs.lakebridge.reconcile.fingerprint.spark_target import build_target_filter_subquery
from databricks.labs.lakebridge.reconcile.recon_config import Schema

_COLUMNS = [
    Schema("`notes`", "varchar", '"notes"'),
    Schema("`is_priority`", "boolean", '"is_priority"'),
]
_SUB_BUCKET_COUNT = 2048

_CONCAT = (
    "COALESCE(TRIM(\"notes\"), '_null_recon_')"
    + " || CHR(1) || "
    + "COALESCE(CASE WHEN \"is_priority\" THEN 'true' WHEN NOT \"is_priority\" THEN 'false' ELSE NULL END,"
    + " '_null_recon_')"
)
_RH1 = f"STRTOL(SUBSTRING(MD5({_CONCAT}), 1, 8), 16)"
_RH2 = f"STRTOL(SUBSTRING(MD5({_CONCAT}), 9, 8), 16)"
_SB_EXPR = f"ABS(MOD({_RH1}, {_SUB_BUCKET_COUNT}))"

_EXPECTED_DETECTION = (
    f"SELECT {_SB_EXPR} AS sub_bucket_id, "
    f"COUNT(*) AS cnt, "
    f"SUM(CAST({_RH1} AS DECIMAL(38,0))) AS p1, "
    f"SUM(CAST({_RH1} AS DECIMAL(19,0)) * CAST({_RH1} AS DECIMAL(19,0))) AS p2, "
    f"SUM(CAST({_RH2} AS DECIMAL(38,0))) AS p1_rh2, "
    f"SUM(CAST({_RH2} AS DECIMAL(19,0)) * CAST({_RH2} AS DECIMAL(19,0))) AS p2_rh2 "
    f'FROM "public"."orders" '
    f"GROUP BY sub_bucket_id"
)


def test_build_detection_sql_golden() -> None:
    builder = RedshiftFingerprintQueryBuilder()
    sql = builder.build_detection_sql(
        schema="public",
        table="orders",
        columns=_COLUMNS,
        column_mapping=None,
        sub_bucket_count=_SUB_BUCKET_COUNT,
    )
    assert sql == _EXPECTED_DETECTION


def test_build_detection_sql_ignores_column_mapping_on_source() -> None:
    builder = RedshiftFingerprintQueryBuilder()
    mapped = builder.build_detection_sql(
        schema="public",
        table="orders",
        columns=_COLUMNS,
        column_mapping={"notes": "tgt_notes", "is_priority": "tgt_priority"},
        sub_bucket_count=_SUB_BUCKET_COUNT,
    )
    assert mapped == _EXPECTED_DETECTION


def test_build_source_filter_subquery_golden() -> None:
    builder = RedshiftFingerprintQueryBuilder()
    sql = builder.build_source_filter_subquery(
        schema="public",
        table="orders",
        columns=_COLUMNS,
        sub_bucket_count=_SUB_BUCKET_COUNT,
        solved_hashes={5: [111, 222]},
        unsolved_sb_ids=[7],
    )
    expected_where = f"({_SB_EXPR} IN (5) AND {_RH1} IN (111, 222)) OR {_SB_EXPR} IN (7)"
    expected = f'(SELECT * FROM "public"."orders" WHERE {expected_where}) _fp_filtered'
    assert sql == expected


def test_build_concat_expression_golden() -> None:
    builder = RedshiftFingerprintQueryBuilder()
    assert builder.build_concat_expression(_COLUMNS) == _CONCAT


_TGT_CONCAT = (
    "CONCAT("
    + "COALESCE(TRIM(`notes`), '_null_recon_'), "
    + "CHAR(1), "
    + "COALESCE(TRIM(`is_priority`), '_null_recon_'))"
)
_TGT_RH1 = f"CAST(CONV(SUBSTR(MD5({_TGT_CONCAT}), 1, 8), 16, 10) AS BIGINT)"
_TGT_SB_EXPR = f"ABS(MOD({_TGT_RH1}, {_SUB_BUCKET_COUNT}))"


def test_build_target_filter_subquery_golden() -> None:
    sql = build_target_filter_subquery(
        "main",
        "perf_test",
        "orders",
        _COLUMNS,
        None,
        {5: [111, 222]},
        [7],
        sub_bucket_count=_SUB_BUCKET_COUNT,
    )
    expected_where = f"({_TGT_SB_EXPR} IN (5) AND {_TGT_RH1} IN (111, 222)) OR {_TGT_SB_EXPR} IN (7)"
    expected = f"(SELECT * FROM `main`.`perf_test`.`orders` WHERE {expected_where}) _fp_filtered"
    assert sql == expected


def test_detection_sql_quotes_exotic_schema_and_table() -> None:
    builder = RedshiftFingerprintQueryBuilder()
    sql = builder.build_detection_sql(
        schema='my"schema',
        table="my-table",
        columns=_COLUMNS,
        column_mapping=None,
        sub_bucket_count=_SUB_BUCKET_COUNT,
    )
    assert 'FROM "my""schema"."my-table"' in sql
