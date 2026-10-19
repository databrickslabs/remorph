"""Unit tests for ``orchestrator.fetch_source_rows`` Stage-2 source-fetch behaviour."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from databricks.labs.lakebridge.reconcile.fingerprint import orchestrator as orch
from databricks.labs.lakebridge.reconcile.fingerprint.metadata import FETCH_PATH_V1_SANDWICH
from databricks.labs.lakebridge.reconcile.fingerprint.query_builders.redshift import (
    RedshiftFingerprintQueryBuilder,
)
from tests.unit.reconcile.fingerprint._fixtures import (
    assert_project_all_columns_kwargs,
    make_fake_hash_builder,
    make_fetch_ctx,
)

_FAKE_HASH_QUERY_PG_FORM = (
    'SELECT LOWER(SHA2(COALESCE(TRIM(CAST("order_amount"::TEXT AS VARCHAR(65535))), '
    "'_null_recon_') || COALESCE(TRIM(CAST(\"order_id\"::TEXT AS VARCHAR(65535))), "
    "'_null_recon_'), 256)) AS hash_value_recon, \"order_id\" AS \"order_id\" FROM %(tbl)s"
)
_FAKE_HASH_QUERY_NAMED_FORM = _FAKE_HASH_QUERY_PG_FORM.replace("%(tbl)s", ":tbl")
_FAKE_HASH_QUERY = _FAKE_HASH_QUERY_PG_FORM

_FAKE_SOURCE_FILTER_SUBQUERY = (
    '(SELECT * FROM "public"."orders" WHERE STRTOL(SUBSTRING(MD5(<concat>), 1, 8), 16) IN (1, 2, 3)) _fp_filtered'
)


def _make_redshift_query_builder():
    builder = RedshiftFingerprintQueryBuilder()
    builder.build_source_filter_subquery = MagicMock(  # type: ignore[method-assign]
        return_value=_FAKE_SOURCE_FILTER_SUBQUERY,
    )
    return builder


def _make_legacy_query_builder():
    builder = MagicMock()
    builder.build_source_filter_subquery.return_value = _FAKE_SOURCE_FILTER_SUBQUERY
    return builder


@pytest.fixture(name="source_mock")
def fixture_source_mock():
    source = MagicMock()
    source.read_data.return_value = MagicMock()
    return source


def _make_fetch_ctx(source, query_builder):
    return make_fetch_ctx(source=source, query_builder=query_builder)


def _patched_fetch_source_rows(*args, **kwargs):
    fake_hash_builder = make_fake_hash_builder(_FAKE_HASH_QUERY)
    with patch.object(orch, "HashQueryBuilder", return_value=fake_hash_builder):
        return orch.fetch_source_rows(*args, **kwargs)


def test_redshift_dialect_emits_single_statement_sandwich(source_mock):
    ctx = _make_fetch_ctx(source_mock, _make_redshift_query_builder())

    df, fetch_path = _patched_fetch_source_rows(
        ctx,
        solved_hashes={1: [10, 20]},
        unsolved_sb_ids=[],
        report_type="data",
    )

    assert df is source_mock.read_data.return_value
    assert fetch_path == FETCH_PATH_V1_SANDWICH
    source_mock.read_data.assert_called_once()

    query = source_mock.read_data.call_args.kwargs["query"]

    assert query.lstrip().upper().startswith("SELECT "), query
    assert "WITH " not in query.upper().split("FROM", 1)[0], "no CTE prefix expected"
    assert "_fp_filtered" in query, query
    assert _FAKE_SOURCE_FILTER_SUBQUERY in query, query
    assert "SHA2" in query.upper()
    assert "hash_value_recon" in query
    assert ":tbl" not in query
    assert "%(tbl)s" not in query
    assert "OFFSET 0" not in query.upper()
    assert "_fp_md5_" not in query
    assert " AS MATERIALIZED " not in query.upper()
    assert "CREATE TEMP TABLE" not in query.upper()
    assert "CREATE TABLE" not in query.upper()


def test_non_redshift_dialect_uses_same_sandwich_shape(source_mock):
    ctx = _make_fetch_ctx(source_mock, _make_legacy_query_builder())

    df, fetch_path = _patched_fetch_source_rows(
        ctx,
        solved_hashes={1: [10, 20]},
        unsolved_sb_ids=[],
        report_type="data",
    )

    assert df is source_mock.read_data.return_value
    assert fetch_path == FETCH_PATH_V1_SANDWICH
    source_mock.read_data.assert_called_once()

    query = source_mock.read_data.call_args.kwargs["query"]
    assert "_fp_filtered" in query
    assert ":tbl" not in query
    assert "%(tbl)s" not in query
    assert "OFFSET 0" not in query.upper()
    assert "_fp_md5_" not in query


def test_fetch_uses_standard_read_data_signature(source_mock):
    ctx = _make_fetch_ctx(source_mock, _make_redshift_query_builder())

    _patched_fetch_source_rows(
        ctx,
        solved_hashes={1: [10]},
        unsolved_sb_ids=[],
        report_type="data",
    )

    kwargs = source_mock.read_data.call_args.kwargs
    assert set(kwargs) == {"catalog", "schema", "table", "query", "options"}
    assert kwargs["catalog"] == "source_catalog"
    assert kwargs["schema"] == "public"
    assert kwargs["table"] == "orders"
    if hasattr(source_mock, "read_data_with_prepare_query"):
        source_mock.read_data_with_prepare_query.assert_not_called()


def test_fetch_passes_jdbc_reader_options_through(source_mock):
    ctx = _make_fetch_ctx(source_mock, _make_redshift_query_builder())

    _patched_fetch_source_rows(
        ctx,
        solved_hashes={1: [10]},
        unsolved_sb_ids=[],
        report_type="data",
    )

    kwargs = source_mock.read_data.call_args.kwargs
    assert "options" in kwargs
    assert kwargs["options"] is None


def test_fetch_invokes_filter_subquery_builder_with_tier_and_solver_outputs(source_mock):
    builder = _make_redshift_query_builder()
    ctx = _make_fetch_ctx(source_mock, builder)

    _patched_fetch_source_rows(
        ctx,
        solved_hashes={5: [101, 102], 9: [203]},
        unsolved_sb_ids=[7, 13],
        report_type="data",
    )

    builder.build_source_filter_subquery.assert_called_once()
    call_kwargs = builder.build_source_filter_subquery.call_args.kwargs
    assert call_kwargs["sub_bucket_count"] == 2_097_152
    assert call_kwargs["solved_hashes"] == {5: [101, 102], 9: [203]}
    assert call_kwargs["unsolved_sb_ids"] == [7, 13]
    assert call_kwargs["schema"] == "public"
    assert call_kwargs["table"] == "orders"


@pytest.mark.parametrize(
    "hash_query_template",
    [_FAKE_HASH_QUERY_NAMED_FORM, _FAKE_HASH_QUERY_PG_FORM],
    ids=["spark-named-:tbl", "redshift-pyformat-%(tbl)s"],
)
def test_fetch_resolves_both_placeholder_forms_for_dialect_parity(source_mock, hash_query_template):
    fake_hash_builder = make_fake_hash_builder(hash_query_template)

    ctx = _make_fetch_ctx(source_mock, _make_redshift_query_builder())
    with patch.object(orch, "HashQueryBuilder", return_value=fake_hash_builder):
        orch.fetch_source_rows(
            ctx,
            solved_hashes={1: [10, 20]},
            unsolved_sb_ids=[],
            report_type="data",
        )

    query = source_mock.read_data.call_args.kwargs["query"]
    assert _FAKE_SOURCE_FILTER_SUBQUERY in query
    assert "_fp_filtered" in query
    assert ":tbl" not in query
    assert "%(tbl)s" not in query


def test_real_redshift_hash_query_builder_emits_pyformat_placeholder():
    sample = "SELECT ... FROM %(tbl)s WHERE ..."
    assert "%(tbl)s" in sample


def test_fetch_source_rows_passes_project_all_columns_true(source_mock):
    fake_hash_builder = make_fake_hash_builder(_FAKE_HASH_QUERY)

    ctx = _make_fetch_ctx(source_mock, _make_redshift_query_builder())
    with patch.object(orch, "HashQueryBuilder", return_value=fake_hash_builder):
        orch.fetch_source_rows(
            ctx,
            solved_hashes={1: [10, 20]},
            unsolved_sb_ids=[],
            report_type="data",
        )

    fake_hash_builder.build_query.assert_called_once()
    assert_project_all_columns_kwargs(fake_hash_builder.build_query.call_args.kwargs, side="source")
