"""Regression tests: ``fetch_source_and_target_rows`` (serial Stage-2 dispatch)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from databricks.labs.lakebridge.reconcile.fingerprint import orchestrator as orch
from databricks.labs.lakebridge.reconcile.fingerprint.metadata import FETCH_PATH_V1_SANDWICH


@pytest.fixture(name="fetch_ctx")
def fixture_fetch_ctx():
    return MagicMock(name="fetch_ctx")


def test_fetch_returns_serial_equivalent_tuple(fetch_ctx):
    fake_src_df = MagicMock(name="src_df")
    fake_tgt_df = MagicMock(name="tgt_df")

    with (
        patch.object(orch, "fetch_source_rows", return_value=(fake_src_df, FETCH_PATH_V1_SANDWICH)),
        patch.object(orch, "fetch_target_rows", return_value=fake_tgt_df),
    ):
        result = orch.fetch_source_and_target_rows(fetch_ctx, solved_hashes={}, unsolved_sb_ids=[1], report_type="data")

    assert isinstance(result, tuple)
    assert len(result) == 3, f"helper must return a 3-tuple (src_df, fetch_path, tgt_df), got {len(result)}-tuple"
    src_df, fetch_path, tgt_df = result
    assert src_df is fake_src_df
    assert fetch_path == FETCH_PATH_V1_SANDWICH
    assert tgt_df is fake_tgt_df


def test_fetch_reraises_source_failure(fetch_ctx):
    boom = RuntimeError("simulated JDBC connection drop")

    with (
        patch.object(orch, "fetch_source_rows", side_effect=boom),
        patch.object(orch, "fetch_target_rows", return_value=MagicMock(name="tgt_df")),
    ):
        with pytest.raises(RuntimeError, match="simulated JDBC connection drop"):
            orch.fetch_source_and_target_rows(fetch_ctx, solved_hashes={}, unsolved_sb_ids=[1], report_type="data")


def test_fetch_reraises_target_failure(fetch_ctx):
    boom = RuntimeError("simulated Delta read failure")

    with (
        patch.object(orch, "fetch_source_rows", return_value=(MagicMock(name="src_df"), FETCH_PATH_V1_SANDWICH)),
        patch.object(orch, "fetch_target_rows", side_effect=boom),
    ):
        with pytest.raises(RuntimeError, match="simulated Delta read failure"):
            orch.fetch_source_and_target_rows(fetch_ctx, solved_hashes={}, unsolved_sb_ids=[1], report_type="data")


def test_fetch_passes_arguments_through_unmodified(fetch_ctx):
    solved = {5: [101, 102], 9: [203]}
    unsolved = [7, 13]

    with (
        patch.object(orch, "fetch_source_rows", return_value=(MagicMock(), FETCH_PATH_V1_SANDWICH)) as src_spy,
        patch.object(orch, "fetch_target_rows", return_value=MagicMock()) as tgt_spy,
    ):
        orch.fetch_source_and_target_rows(fetch_ctx, solved, unsolved, "data")

    src_spy.assert_called_once_with(fetch_ctx, solved, unsolved, "data")
    tgt_spy.assert_called_once_with(fetch_ctx, solved, unsolved, "data")
