"""Regression tests for the ``detect_and_solve`` Stage-1 caching contract."""

from __future__ import annotations

import ast
import inspect
import textwrap
from unittest.mock import MagicMock, call

import pytest

from databricks.labs.lakebridge.reconcile.fingerprint import engine
from databricks.labs.lakebridge.reconcile.fingerprint.engine import detect_and_solve


def _function_calls(func):
    source = textwrap.dedent(inspect.getsource(func))
    tree = ast.parse(source)
    calls: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            inner = node.func.value
            if isinstance(inner, ast.Name):
                calls.append(f"{inner.id}.{node.func.attr}")
    return calls


def _function_body_text(func) -> str:
    source = textwrap.dedent(inspect.getsource(func))
    tree = ast.parse(source)
    func_node = tree.body[0]
    assert isinstance(func_node, (ast.FunctionDef, ast.AsyncFunctionDef))
    if (
        func_node.body
        and isinstance(func_node.body[0], ast.Expr)
        and isinstance(func_node.body[0].value, ast.Constant)
        and isinstance(func_node.body[0].value.value, str)
    ):
        func_node.body = func_node.body[1:]
    return ast.unparse(func_node)


def _build_chain(*, total_sbs: int, mismatch_count: int):
    joined = MagicMock(name="joined_select")

    select_chain = MagicMock(name="select_chain")
    select_chain.cache.return_value = joined

    join_chain = MagicMock(name="join_chain")
    join_chain.select.return_value = select_chain

    src = MagicMock(name="source_agg_df")
    src_alias = MagicMock(name="source_alias")
    src_alias.join.return_value = join_chain
    src.alias.return_value = src_alias

    tgt = MagicMock(name="target_agg_df")
    tgt.alias.return_value = MagicMock(name="target_alias")

    counts_row = MagicMock(name="counts_row")
    counts_row.__getitem__.side_effect = lambda key: {
        "total_sbs": total_sbs,
        "mismatch_count": mismatch_count,
    }[key]

    agg_result = MagicMock(name="agg_result")
    agg_result.collect.return_value = [counts_row]

    joined.agg.return_value = agg_result
    joined.filter.return_value = MagicMock(name="mismatched", **{"collect.return_value": []})
    return src, tgt, joined


def test_match_path_caches_and_unpersists():
    src, tgt, joined = _build_chain(total_sbs=1024, mismatch_count=0)

    result = detect_and_solve(src, tgt)

    assert result.verdict == "MATCH"
    src.alias.return_value.join.return_value.select.return_value.cache.assert_called_once_with()
    joined.unpersist.assert_called_once_with()


def test_systemic_mismatch_path_unpersists():
    src, tgt, joined = _build_chain(total_sbs=300, mismatch_count=60)

    result = detect_and_solve(src, tgt)

    assert result.verdict == "MISMATCH"
    assert result.systemic_mismatch is True
    joined.unpersist.assert_called_once_with()
    joined.filter.return_value.collect.assert_not_called()


def test_small_table_ratio_alone_does_not_trigger_systemic_guard():
    src, tgt, joined = _build_chain(total_sbs=6, mismatch_count=1)

    result = detect_and_solve(src, tgt)

    assert result.verdict == "MISMATCH"
    assert result.systemic_mismatch is False
    joined.filter.return_value.collect.assert_called_once_with()
    joined.unpersist.assert_called_once_with()


def test_solver_mismatch_path_unpersists():
    src, tgt, joined = _build_chain(total_sbs=1024, mismatch_count=1)

    result = detect_and_solve(src, tgt)

    assert result.verdict == "MISMATCH"
    assert result.systemic_mismatch is False
    joined.filter.return_value.collect.assert_called_once_with()
    joined.unpersist.assert_called_once_with()


def test_solver_path_uses_cached_frame_only_once_for_counts():
    src, tgt, joined = _build_chain(total_sbs=1024, mismatch_count=0)

    detect_and_solve(src, tgt)

    assert joined.agg.call_count == 1
    assert joined.count.call_count == 0, "joined.count() reintroduced — single-agg Stage-1 contract broken"
    assert (
        joined.filter.return_value.count.call_count == 0
    ), "mismatched.count() reintroduced — single-agg Stage-1 contract broken"


def test_unpersist_runs_even_when_solver_path_raises():
    src, tgt, joined = _build_chain(total_sbs=1024, mismatch_count=1)
    joined.filter.return_value.collect.side_effect = RuntimeError("simulated executor failure")

    with pytest.raises(RuntimeError, match="simulated executor failure"):
        detect_and_solve(src, tgt)

    joined.unpersist.assert_called_once_with()


def test_source_inspection_documents_single_agg_pattern():
    body = _function_body_text(engine.detect_and_solve)
    calls = _function_calls(engine.detect_and_solve)

    assert ".cache()" in body, "joined frame must be cached before any Spark action"
    assert "_cached_frame(joined)" in body, (
        "joined frame must be wrapped in the _cached_frame(...) context manager so it is "
        "released on every return path (the behavioural test above asserts the actual unpersist call)"
    )
    assert "joined.count" not in calls, (
        "single-agg Stage-1 contract violated: detect_and_solve calls joined.count() — "
        "fold into the existing joined.agg(...) instead"
    )
    assert "mismatched.count" not in calls, (
        "single-agg Stage-1 contract violated: detect_and_solve calls mismatched.count() — "
        "fold into the existing joined.agg(...) using F.when(condition, 1).otherwise(0)"
    )
    assert "joined.agg" in calls, "single-agg Stage-1 contract requires joined.agg(...)"


def test_counts_row_reads_total_and_mismatch_keys():
    src, tgt, joined = _build_chain(total_sbs=10, mismatch_count=0)
    detect_and_solve(src, tgt)

    counts_row = joined.agg.return_value.collect.return_value[0]
    assert call("total_sbs") in counts_row.__getitem__.call_args_list
    assert call("mismatch_count") in counts_row.__getitem__.call_args_list
