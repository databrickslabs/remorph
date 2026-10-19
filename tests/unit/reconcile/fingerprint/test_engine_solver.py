"""Unit tests for fingerprint algebraic solver helpers."""

import inspect
from decimal import Decimal

import pytest

from databricks.labs.lakebridge.reconcile.fingerprint import engine
from databricks.labs.lakebridge.reconcile.fingerprint.engine import solve_d1, solve_d2_swap


def test_solve_d1_uses_abs_of_delta():
    result_neg = solve_d1(1, -1, -42, -1764, -10, -100)
    assert result_neg is not None
    assert result_neg.target_hashes == [42]
    assert not result_neg.source_hashes

    result_pos = solve_d1(2, 1, 99, 9801, 50, 2500)
    assert result_pos is not None
    assert result_pos.source_hashes == [99]


def test_solve_d1_rejects_wrong_p2():
    assert solve_d1(1, 1, 42, 9999, 10, 100) is None


def test_solve_d2_swap_basic():
    result = solve_d2_swap(1, 2, 16, 4, 40)
    assert result is not None
    assert result.source_hashes == [5]
    assert result.target_hashes == [3]


def test_detect_and_solve_mismatch_filter_covers_rh2_channel():
    src = inspect.getsource(engine.detect_and_solve)
    assert 'F.col("src_p1_rh2") != F.col("tgt_p1_rh2")' in src
    assert 'F.col("src_p2_rh2") != F.col("tgt_p2_rh2")' in src


def test_solve_d2_extras_handles_target_side_negative_d_cnt():
    h_a, h_b = 5, 3
    d_cnt = -2
    d_p1 = -(h_a + h_b)
    d_p2 = -(h_a * h_a + h_b * h_b)
    rh2_a, rh2_b = 7, 11
    d_p1_rh2 = -(rh2_a + rh2_b)
    d_p2_rh2 = -(rh2_a * rh2_a + rh2_b * rh2_b)

    result = engine.solve_sub_bucket(
        sb_id=99,
        d_cnt=d_cnt,
        d_p1=d_p1,
        d_p2=d_p2,
        d_p1_rh2=d_p1_rh2,
        d_p2_rh2=d_p2_rh2,
    )

    assert result is not None
    assert not result.source_hashes
    assert sorted(result.target_hashes) == [3, 5]


def test_solve_d2_swap_rejects_weak_rh2_cross_verify():
    assert solve_d2_swap(sb_id=42, d_p1=2, d_p2=16, d_p1_rh2=2, d_p2_rh2=10) is None


def test_solve_d2_swap_rejects_odd_parity_delta():
    assert solve_d2_swap(42, d_p1=2, d_p2=6, d_p1_rh2=0, d_p2_rh2=0) is None


def test_solve_d2_swap_rejects_out_of_range_root():
    h_old = 0x1_0000_0000
    h_new = 0
    d_p1 = h_old - h_new
    d_p2 = h_old * h_old - h_new * h_new
    assert solve_d2_swap(7, d_p1, d_p2, d_p1_rh2=0, d_p2_rh2=0) is None


def test_solve_d2_swap_rejects_negative_root_product():
    assert solve_d2_swap(11, d_p1=12, d_p2=96, d_p1_rh2=0, d_p2_rh2=0) is None


def test_solve_d2_extras_dedupes_repeated_root():
    result = solve_d1.__globals__["_solve_d2_extras"](
        sb_id=5,
        d_cnt=2,
        d_p1=8,
        d_p2=32,
        d_p1_rh2=8,
        d_p2_rh2=32,
    )
    assert result is not None
    assert result.source_hashes == [4]
    assert not result.target_hashes


def test_solve_d2_extras_rejects_decimal_inputs():
    with pytest.raises(TypeError, match="decimal.Decimal"):
        solve_d1.__globals__["_solve_d2_extras"](
            sb_id=5,
            d_cnt=2,
            d_p1=Decimal(8),
            d_p2=Decimal(32),
            d_p1_rh2=Decimal(8),
            d_p2_rh2=Decimal(32),
        )


def test_detect_and_solve_casts_row_values_to_int():
    src = inspect.getsource(engine.detect_and_solve)
    for cast_expr in (
        'int(row["sub_bucket_id"])',
        'int(row["src_cnt"])',
        'int(row["tgt_cnt"])',
        'int(row["src_p1"])',
        'int(row["tgt_p1"])',
        'int(row["src_p2"])',
        'int(row["tgt_p2"])',
        'int(row["src_p1_rh2"])',
        'int(row["tgt_p1_rh2"])',
        'int(row["src_p2_rh2"])',
        'int(row["tgt_p2_rh2"])',
    ):
        assert cast_expr in src, f"detect_and_solve row loop is missing {cast_expr}"
