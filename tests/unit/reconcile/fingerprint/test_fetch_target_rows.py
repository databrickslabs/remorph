"""Unit tests for ``orchestrator.fetch_target_rows`` Stage-2 target-fetch behaviour."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from databricks.labs.lakebridge.reconcile.fingerprint import orchestrator as orch
from tests.unit.reconcile.fingerprint._fixtures import (
    assert_project_all_columns_kwargs,
    make_fake_hash_builder,
    make_fetch_ctx,
)

_FAKE_TGT_HASH_QUERY_NAMED_FORM = (
    'SELECT LOWER(SHA2(COALESCE(TRIM(CAST(`order_amount` AS STRING)), '
    "'_null_recon_') || COALESCE(TRIM(CAST(`order_id` AS STRING)), "
    "'_null_recon_'), 256)) AS hash_value_recon, `order_id` AS `order_id` FROM :tbl"
)
_FAKE_TGT_HASH_QUERY_PG_FORM = _FAKE_TGT_HASH_QUERY_NAMED_FORM.replace(":tbl", "%(tbl)s")
_FAKE_TGT_HASH_QUERY = _FAKE_TGT_HASH_QUERY_NAMED_FORM

_FAKE_TARGET_FILTER_SUBQUERY = (
    "(SELECT * FROM test_catalog.perf_test.orders "
    "WHERE ABS(MOD(CAST(CONV(SUBSTR(MD5(<concat>), 1, 8), 16, 10) AS BIGINT), 2097152)) "
    "IN (1, 2, 3)) _fp_filtered"
)


@pytest.fixture(name="target_mock")
def fixture_target_mock():
    target = MagicMock()
    target.read_data.return_value = MagicMock()
    return target


def _make_fetch_ctx(target):
    return make_fetch_ctx(target=target)


def _patched_fetch_target_rows(*args, hash_query: str = _FAKE_TGT_HASH_QUERY, **kwargs):
    fake_hash_builder = make_fake_hash_builder(hash_query)
    with (
        patch.object(orch, "HashQueryBuilder", return_value=fake_hash_builder),
        patch.object(orch, "build_target_filter_subquery", return_value=_FAKE_TARGET_FILTER_SUBQUERY),
    ):
        return orch.fetch_target_rows(*args, **kwargs)


def test_target_fetch_emits_single_statement_sandwich(target_mock):
    ctx = _make_fetch_ctx(target_mock)

    df = _patched_fetch_target_rows(
        ctx,
        solved_hashes={1: [10, 20]},
        unsolved_sb_ids=[],
        report_type="data",
    )

    assert df is target_mock.read_data.return_value
    target_mock.read_data.assert_called_once()

    kwargs = target_mock.read_data.call_args.kwargs
    query = kwargs["query"]

    assert query.lstrip().upper().startswith("SELECT "), query
    assert "WITH " not in query.upper().split("FROM", 1)[0], "no CTE prefix expected on sandwich path"
    assert "_fp_filtered" in query, query
    assert _FAKE_TARGET_FILTER_SUBQUERY in query, query
    assert "SHA2" in query.upper()
    assert "hash_value_recon" in query
    assert ":tbl" not in query
    assert "%(tbl)s" not in query


def test_target_fetch_uses_standard_read_data_signature(target_mock):
    ctx = _make_fetch_ctx(target_mock)

    _patched_fetch_target_rows(
        ctx,
        solved_hashes={1: [10]},
        unsolved_sb_ids=[],
        report_type="data",
    )

    kwargs = target_mock.read_data.call_args.kwargs
    assert set(kwargs) == {"catalog", "schema", "table", "query", "options"}
    assert kwargs["catalog"] == "test_catalog"
    assert kwargs["schema"] == "perf_test"
    assert kwargs["table"] == "orders"
    assert kwargs["options"] is None


def test_target_fetch_invokes_filter_subquery_with_tier_and_solver_outputs(target_mock):
    ctx = _make_fetch_ctx(target_mock)
    fake_hash_builder = make_fake_hash_builder(_FAKE_TGT_HASH_QUERY)
    with (
        patch.object(orch, "HashQueryBuilder", return_value=fake_hash_builder),
        patch.object(orch, "build_target_filter_subquery", return_value=_FAKE_TARGET_FILTER_SUBQUERY) as filter_builder,
    ):
        orch.fetch_target_rows(
            ctx,
            solved_hashes={5: [101, 102], 9: [203]},
            unsolved_sb_ids=[7, 13],
            report_type="data",
        )

    filter_builder.assert_called_once()
    args, call_kwargs = filter_builder.call_args
    assert call_kwargs["sub_bucket_count"] == 2_097_152, (
        "Stage-2 target fetch must use the same adaptive sub_bucket_count as "
        "Stage-1 detection — otherwise the target WHERE predicate's sub-bucket "
        "modulus won't match the IDs the solver produced and the filter "
        "returns no rows (silent MATCH false positive)."
    )
    assert args[5] == {5: [101, 102], 9: [203]}, "solved_hashes must reach the helper unchanged"
    assert args[6] == [7, 13], "unsolved_sb_ids must reach the helper unchanged"


@pytest.mark.parametrize(
    "hash_query_template",
    [_FAKE_TGT_HASH_QUERY_NAMED_FORM, _FAKE_TGT_HASH_QUERY_PG_FORM],
    ids=["spark-named-:tbl", "pyformat-%(tbl)s"],
)
def test_target_fetch_resolves_both_placeholder_forms_for_dialect_parity(target_mock, hash_query_template):
    ctx = _make_fetch_ctx(target_mock)

    _patched_fetch_target_rows(
        ctx,
        solved_hashes={1: [10, 20]},
        unsolved_sb_ids=[],
        report_type="data",
        hash_query=hash_query_template,
    )

    query = target_mock.read_data.call_args.kwargs["query"]
    assert _FAKE_TARGET_FILTER_SUBQUERY in query
    assert "_fp_filtered" in query
    assert ":tbl" not in query
    assert "%(tbl)s" not in query, (
        "Bug-R parity guard: even though Spark dialect emits ``:tbl`` today, "
        "the defensive ``replace('%(tbl)s', ...)`` at orchestrator line ~480 "
        "must remain. A future sqlglot bump that changes Spark rendering to "
        "``FROM %(tbl)s`` would otherwise silently leave the placeholder for "
        "the connector to substitute with the bare ``<schema>.<table>``, "
        "scanning the entire Delta target instead of the filtered subset and "
        "producing phantom ``missing_in_source`` counts in production "
        "``recon_metrics`` rows."
    )


def test_target_fetch_no_w2b_machinery_leakage(target_mock):
    ctx = _make_fetch_ctx(target_mock)

    _patched_fetch_target_rows(
        ctx,
        solved_hashes={1: [10, 20]},
        unsolved_sb_ids=[],
        report_type="data",
    )

    query = target_mock.read_data.call_args.kwargs["query"]
    assert "OFFSET 0" not in query.upper(), "OFFSET 0 fence reverted on 0.12.8"
    assert "_fp_md5_" not in query, "v2 CTE name pattern reverted on 0.12.8"
    assert " AS MATERIALIZED " not in query.upper()
    assert "CREATE TEMP TABLE" not in query.upper()
    assert "CREATE TABLE" not in query.upper()


def test_target_fetch_passes_project_all_columns_true(target_mock):
    fake_hash_builder = make_fake_hash_builder(_FAKE_TGT_HASH_QUERY)

    ctx = _make_fetch_ctx(target_mock)
    with (
        patch.object(orch, "HashQueryBuilder", return_value=fake_hash_builder),
        patch.object(orch, "build_target_filter_subquery", return_value=_FAKE_TARGET_FILTER_SUBQUERY),
    ):
        orch.fetch_target_rows(
            ctx,
            solved_hashes={1: [10, 20]},
            unsolved_sb_ids=[],
            report_type="data",
        )

    fake_hash_builder.build_query.assert_called_once()
    assert_project_all_columns_kwargs(fake_hash_builder.build_query.call_args.kwargs, side="target")
