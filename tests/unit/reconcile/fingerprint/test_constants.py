"""Unit tests for fingerprint adaptive sub-bucket sizing."""

from __future__ import annotations

import pytest

from databricks.labs.lakebridge.reconcile.fingerprint.constants import (
    BUCKET_COUNT,
    SUB_BUCKET_COUNT,
    SUB_BUCKET_TIERS,
    build_fingerprint_where_clause,
    pick_sub_bucket_count,
)


def test_sub_bucket_tiers_max_row_count_is_strictly_monotonic() -> None:
    bounded_max_row_counts = [t[0] for t in SUB_BUCKET_TIERS if t[0] is not None]
    assert bounded_max_row_counts == sorted(
        bounded_max_row_counts
    ), f"SUB_BUCKET_TIERS rows must be ordered by ascending max_row_count; got {bounded_max_row_counts}"
    assert len(set(bounded_max_row_counts)) == len(
        bounded_max_row_counts
    ), "Duplicate max_row_count values make later entries unreachable in pick_sub_bucket_count."
    assert SUB_BUCKET_TIERS[-1][0] is None, "Last tier must be open-ended (max_row_count=None)"
    assert sum(1 for t in SUB_BUCKET_TIERS if t[0] is None) == 1, "Exactly one open-ended tier permitted"


def test_sub_bucket_tiers_sub_bucket_counts_are_powers_of_two() -> None:
    for max_rc, sub_buckets, _bucket_count in SUB_BUCKET_TIERS:
        assert (
            sub_buckets > 0 and (sub_buckets & (sub_buckets - 1)) == 0
        ), f"sub_bucket_count {sub_buckets} (tier max_row_count={max_rc}) is not a power of 2"


@pytest.mark.parametrize(
    ("row_count", "expected_sub_buckets", "expected_buckets"),
    [
        (1, 16_384, 128),
        (10_000, 16_384, 128),
        (50_000, 16_384, 128),
        (50_001, 262_144, 512),
        (100_000, 262_144, 512),
        (500_000, 262_144, 512),
        (500_001, 1_048_576, 1_024),
        (10_000_000, 1_048_576, 1_024),
        (50_000_000, 1_048_576, 1_024),
        (50_000_001, 2_097_152, 2_048),
        (100_000_000, 2_097_152, 2_048),
        (500_000_000, 2_097_152, 2_048),
        (500_000_001, 4_194_304, 4_096),
        (1_000_000_000, 4_194_304, 4_096),
        (5_000_000_000, 4_194_304, 4_096),
        (5_000_000_001, 8_388_608, 8_192),
        (15_800_000_000, 8_388_608, 8_192),
        (20_000_000_000, 8_388_608, 8_192),
        (50_000_000_000, 8_388_608, 8_192),
        (50_000_000_001, 16_777_216, 16_384),
        (100_000_000_000, 16_777_216, 16_384),
        (1_000_000_000_000, 16_777_216, 16_384),
    ],
)
def test_pick_sub_bucket_count_tier_table(row_count, expected_sub_buckets, expected_buckets):
    sub_buckets, buckets = pick_sub_bucket_count(row_count)
    assert sub_buckets == expected_sub_buckets
    assert buckets == expected_buckets


@pytest.mark.parametrize("row_count", [None, 0, -1, -100])
def test_pick_sub_bucket_count_falls_back_to_static_default_when_row_count_unknown(row_count):
    sub_buckets, buckets = pick_sub_bucket_count(row_count)
    assert sub_buckets == SUB_BUCKET_COUNT
    assert buckets == BUCKET_COUNT


def test_tier_table_is_monotonic_in_row_count():
    last_sub_buckets = 0
    last_buckets = 0
    for _max_rows, sub_buckets, buckets in SUB_BUCKET_TIERS:
        assert sub_buckets >= last_sub_buckets, f"sub_buckets regressed: {last_sub_buckets} -> {sub_buckets}"
        assert buckets >= last_buckets, f"buckets regressed: {last_buckets} -> {buckets}"
        last_sub_buckets = sub_buckets
        last_buckets = buckets


def _is_power_of_two(value: int) -> bool:
    return value > 0 and (value & (value - 1)) == 0


def test_tier_table_buckets_are_strict_subdivisions_of_sub_buckets():
    for _max_rows, sub_buckets, buckets in SUB_BUCKET_TIERS:
        assert buckets < sub_buckets
        ratio = sub_buckets // buckets
        assert _is_power_of_two(ratio), f"ratio {ratio} for ({sub_buckets}, {buckets}) is not a power of 2"


def test_tier_table_powers_of_two():
    for _max_rows, sub_buckets, buckets in SUB_BUCKET_TIERS:
        assert _is_power_of_two(sub_buckets), f"sub_bucket_count {sub_buckets} is not a power of 2"
        assert _is_power_of_two(buckets), f"bucket_count {buckets} is not a power of 2"


def test_tier_table_final_clamp_is_open_ended():
    assert SUB_BUCKET_TIERS[-1][0] is None


def test_static_defaults_match_legacy_lakebridge_values():
    assert SUB_BUCKET_COUNT == 1_048_576
    assert BUCKET_COUNT == 32_768


def test_where_clause_emits_union_form_for_solved_hashes():
    where = build_fingerprint_where_clause(
        sb_expr="SB(x)",
        rh1_expr="RH(x)",
        solved_hashes={5: [100, 200], 7: [300]},
        unsolved_sb_ids=[],
    )
    assert where == "(SB(x) IN (5, 7) AND RH(x) IN (100, 200, 300))"


def test_where_clause_appends_unsolved_sub_buckets_as_second_disjunct():
    where = build_fingerprint_where_clause(
        sb_expr="SB(x)",
        rh1_expr="RH(x)",
        solved_hashes={5: [100]},
        unsolved_sb_ids=[9, 11],
    )
    assert where == "(SB(x) IN (5) AND RH(x) IN (100)) OR SB(x) IN (9, 11)"


def test_where_clause_handles_only_unsolved_sub_buckets():
    where = build_fingerprint_where_clause(
        sb_expr="SB(x)",
        rh1_expr="RH(x)",
        solved_hashes={},
        unsolved_sb_ids=[1, 2, 3],
    )
    assert where == "SB(x) IN (1, 2, 3)"


def test_where_clause_size_is_constant_in_number_of_solved_sub_buckets():
    fat_sb_expr = "<<SB_EXPR_" + "X" * 2_000 + ">>"
    fat_rh1_expr = "<<RH_EXPR_" + "Y" * 2_000 + ">>"
    solved = {sb_id: [sb_id * 7919 + 1] for sb_id in range(50_000)}

    where = build_fingerprint_where_clause(fat_sb_expr, fat_rh1_expr, solved, [])

    assert len(where) < 1_000_000, f"WHERE clause too large: {len(where):,} bytes"
    assert where.count(fat_sb_expr) == 1, "sb_expr must be emitted exactly once"
    assert where.count(fat_rh1_expr) == 1, "rh1_expr must be emitted exactly once"


def test_where_clause_is_deterministic_across_dict_iteration_orders():
    where_a = build_fingerprint_where_clause("SB", "RH", {3: [30], 1: [10], 2: [20, 21]}, [9, 7, 8])
    where_b = build_fingerprint_where_clause("SB", "RH", {1: [10], 2: [21, 20], 3: [30]}, [8, 9, 7])
    assert where_a == where_b
    assert "(SB IN (1, 2, 3) AND RH IN (10, 20, 21, 30))" in where_a
    assert "SB IN (7, 8, 9)" in where_a


def test_where_clause_sorts_unsolved_sb_ids_for_plan_cache_stability():
    where = build_fingerprint_where_clause("SB", "RH", {}, [42, 7, 13])
    assert where == "SB IN (7, 13, 42)"


def test_where_clause_raises_when_both_filter_inputs_are_empty():
    with pytest.raises(ValueError, match="requires at least one"):
        build_fingerprint_where_clause("SB", "RH", {}, [])
