"""Unit tests for the fingerprint target row-count fetcher."""

from __future__ import annotations

from unittest.mock import MagicMock

from pyspark.sql.utils import AnalysisException

from databricks.labs.lakebridge.reconcile.fingerprint.row_count import (
    RowCountResult,
    RowCountSource,
    fetch_target_row_count,
)


def _make_describe_detail_df(*, columns: list[str], rows: list[dict]) -> MagicMock:
    df = MagicMock()
    df.columns = columns

    if rows is None or "numRecords" not in columns:
        return df

    select_result = MagicMock()
    select_result.collect.return_value = [_RowLike(r) for r in rows]
    df.select.return_value = select_result
    return df


class _RowLike:
    """Mimics PySpark Row ``row['key']`` access."""

    def __init__(self, mapping: dict):
        self._mapping = mapping

    def __getitem__(self, key):
        return self._mapping[key]


_UNSET = object()


def _make_count_df(value) -> MagicMock:
    df = MagicMock()
    df.collect.return_value = [] if value is None else [_RowLike({"cnt": value})]
    return df


def _make_spark(describe_detail_df: MagicMock | Exception, *, count_star=_UNSET) -> MagicMock:

    def _sql(query, *_args, **_kwargs):
        if "COUNT(*)" in query:
            if isinstance(count_star, Exception):
                raise count_star
            return _make_count_df(None if count_star is _UNSET else count_star)
        if isinstance(describe_detail_df, Exception):
            raise describe_detail_df
        return describe_detail_df

    spark = MagicMock()
    spark.sql.side_effect = _sql
    return spark


def test_describe_detail_returns_num_records_for_delta_table():
    df = _make_describe_detail_df(
        columns=["format", "id", "name", "numFiles", "numRecords", "createdAt"],
        rows=[{"numRecords": 100_000_000}],
    )
    spark = _make_spark(df)
    result = fetch_target_row_count(spark, catalog="test_catalog", schema="perf_test", table="orders")
    assert result == RowCountResult(row_count=100_000_000, source=RowCountSource.DELTA_DESCRIBE_DETAIL)
    spark.sql.assert_called_once_with("DESCRIBE DETAIL `test_catalog`.`perf_test`.`orders`")


def test_describe_detail_works_without_catalog():
    df = _make_describe_detail_df(columns=["numRecords"], rows=[{"numRecords": 1_000}])
    spark = _make_spark(df)
    result = fetch_target_row_count(spark, catalog=None, schema="default", table="orders")
    assert result.row_count == 1_000
    spark.sql.assert_called_once_with("DESCRIBE DETAIL `default`.`orders`")


def test_describe_detail_quotes_delimiting_needed_identifiers():
    df = _make_describe_detail_df(columns=["numRecords"], rows=[{"numRecords": 42}])
    spark = _make_spark(df)
    result = fetch_target_row_count(spark, catalog="my-catalog", schema="perf_test", table="order")
    assert result == RowCountResult(row_count=42, source=RowCountSource.DELTA_DESCRIBE_DETAIL)
    spark.sql.assert_called_once_with("DESCRIBE DETAIL `my-catalog`.`perf_test`.`order`")


def test_describe_detail_zero_rows_is_legitimate():
    df = _make_describe_detail_df(columns=["numRecords"], rows=[{"numRecords": 0}])
    spark = _make_spark(df)
    result = fetch_target_row_count(spark, catalog="test_catalog", schema="perf_test", table="orders")
    assert result == RowCountResult(row_count=0, source=RowCountSource.DELTA_DESCRIBE_DETAIL)


def test_count_star_used_when_describe_detail_lacks_num_records():
    describe = _make_describe_detail_df(columns=["format", "numFiles", "sizeInBytes"], rows=[])
    spark = _make_spark(describe, count_star=1_000_000)
    result = fetch_target_row_count(spark, catalog="users", schema="ameer_salman", table="orders_capbound")
    assert result == RowCountResult(row_count=1_000_000, source=RowCountSource.COUNT_STAR)


def test_count_star_used_when_describe_detail_raises():
    spark = _make_spark(AnalysisException("DESCRIBE DETAIL unsupported"), count_star=500)
    result = fetch_target_row_count(spark, catalog="c", schema="s", table="orders")
    assert result == RowCountResult(row_count=500, source=RowCountSource.COUNT_STAR)


def test_count_star_queries_the_backtick_quoted_target_fqn():
    describe = _make_describe_detail_df(columns=["format"], rows=[])
    spark = _make_spark(describe, count_star=7)
    fetch_target_row_count(spark, catalog="my-catalog", schema="perf_test", table="orders")
    count_calls = [c.args[0] for c in spark.sql.call_args_list if "COUNT(*)" in c.args[0]]
    assert count_calls == ["SELECT COUNT(*) AS cnt FROM `my-catalog`.`perf_test`.`orders`"], count_calls


def test_count_star_zero_is_legitimate_empty_table():
    describe = _make_describe_detail_df(columns=["format"], rows=[])
    spark = _make_spark(describe, count_star=0)
    result = fetch_target_row_count(spark, catalog="c", schema="s", table="orders")
    assert result == RowCountResult(row_count=0, source=RowCountSource.COUNT_STAR)


def test_count_star_failure_falls_back_to_static_default():
    describe = _make_describe_detail_df(columns=["format"], rows=[])
    spark = _make_spark(describe, count_star=RuntimeError("executor lost"))
    result = fetch_target_row_count(spark, catalog="c", schema="s", table="orders")
    assert result == RowCountResult(row_count=None, source=RowCountSource.STATIC_DEFAULT)


def test_count_star_non_int_falls_back_to_static_default():
    describe = _make_describe_detail_df(columns=["format"], rows=[])
    spark = _make_spark(describe, count_star="1000000")
    result = fetch_target_row_count(spark, catalog="c", schema="s", table="orders")
    assert result == RowCountResult(row_count=None, source=RowCountSource.STATIC_DEFAULT)


def test_count_star_path_emits_info_log(caplog):
    describe = _make_describe_detail_df(columns=["format"], rows=[])
    spark = _make_spark(describe, count_star=1_000_000)
    with caplog.at_level("INFO"):
        fetch_target_row_count(spark, catalog="c", schema="s", table="orders")
    assert any(
        "row_count_source=count_star" in rec.message and "row_count=1000000" in rec.message for rec in caplog.records
    )


def test_table_not_found_falls_back_to_static_default():
    spark = _make_spark(AnalysisException("Table or view not found: test_catalog.perf_test.bogus"))
    result = fetch_target_row_count(spark, catalog="test_catalog", schema="perf_test", table="bogus")
    assert result == RowCountResult(row_count=None, source=RowCountSource.STATIC_DEFAULT)


def test_unexpected_exception_falls_back_to_static_default():
    spark = _make_spark(RuntimeError("kerberos creds expired"))
    result = fetch_target_row_count(spark, catalog="test_catalog", schema="perf_test", table="orders")
    assert result == RowCountResult(row_count=None, source=RowCountSource.STATIC_DEFAULT)


def test_non_delta_target_with_no_num_records_column_falls_back():
    df = _make_describe_detail_df(
        columns=["format", "id", "name"],
        rows=[],
    )
    spark = _make_spark(df)
    result = fetch_target_row_count(spark, catalog="test_catalog", schema="perf_test", table="orders")
    assert result == RowCountResult(row_count=None, source=RowCountSource.STATIC_DEFAULT)


def test_describe_detail_returning_zero_rows_falls_back():
    df = _make_describe_detail_df(columns=["numRecords"], rows=[])
    spark = _make_spark(df)
    result = fetch_target_row_count(spark, catalog="test_catalog", schema="perf_test", table="orders")
    assert result == RowCountResult(row_count=None, source=RowCountSource.STATIC_DEFAULT)


def test_describe_detail_returning_null_num_records_falls_back():
    df = _make_describe_detail_df(columns=["numRecords"], rows=[{"numRecords": None}])
    spark = _make_spark(df)
    result = fetch_target_row_count(spark, catalog="test_catalog", schema="perf_test", table="orders")
    assert result == RowCountResult(row_count=None, source=RowCountSource.STATIC_DEFAULT)


def test_describe_detail_returning_unexpected_type_falls_back():
    df = _make_describe_detail_df(columns=["numRecords"], rows=[{"numRecords": "100000000"}])
    spark = _make_spark(df)
    result = fetch_target_row_count(spark, catalog="test_catalog", schema="perf_test", table="orders")
    assert result == RowCountResult(row_count=None, source=RowCountSource.STATIC_DEFAULT)


def test_describe_detail_returning_negative_num_records_falls_back():
    df = _make_describe_detail_df(columns=["numRecords"], rows=[{"numRecords": -1}])
    spark = _make_spark(df)
    result = fetch_target_row_count(spark, catalog="test_catalog", schema="perf_test", table="orders")
    assert result == RowCountResult(row_count=None, source=RowCountSource.STATIC_DEFAULT)


def test_static_default_path_emits_warning_log(caplog):
    spark = _make_spark(AnalysisException("not found"))
    with caplog.at_level("WARNING"):
        fetch_target_row_count(spark, catalog="test_catalog", schema="perf_test", table="orders")
    assert any(
        "row_count_source=static_default" in rec.message for rec in caplog.records
    ), "STATIC_DEFAULT fallback must log at WARNING level for operator visibility"


def test_delta_describe_detail_path_emits_info_log(caplog):
    df = _make_describe_detail_df(columns=["numRecords"], rows=[{"numRecords": 100_000_000}])
    spark = _make_spark(df)
    with caplog.at_level("INFO"):
        fetch_target_row_count(spark, catalog="test_catalog", schema="perf_test", table="orders")
    assert any(
        "row_count_source=delta_describe_detail" in rec.message and "row_count=100000000" in rec.message
        for rec in caplog.records
    )
