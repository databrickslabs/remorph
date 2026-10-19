"""Randomized sufficiency + safety guards for the d<=2 algebraic solver."""

import math
import random
from collections import Counter

from databricks.labs.lakebridge.reconcile.fingerprint import engine
from databricks.labs.lakebridge.reconcile.fingerprint.constants import (
    SUB_BUCKET_COUNT,
    SUB_BUCKET_TIERS,
)

_RH_MAX = 0xFFFFFFFF
_SEED = 20260703
_TRIALS = 10_000
_SOLVE_RATE_FLOOR = 0.988


def _solve(src_r1, src_r2, tgt_r1, tgt_r2):
    d_cnt = len(src_r1) - len(tgt_r1)
    d_p1 = sum(src_r1) - sum(tgt_r1)
    d_p2 = sum(h * h for h in src_r1) - sum(h * h for h in tgt_r1)
    d_p1_rh2 = sum(src_r2) - sum(tgt_r2)
    d_p2_rh2 = sum(h * h for h in src_r2) - sum(h * h for h in tgt_r2)
    return engine.solve_sub_bucket(0, d_cnt, d_p1, d_p2, d_p1_rh2, d_p2_rh2)


def _diff_hashes(src_r1, tgt_r1):
    src_counts, tgt_counts = Counter(src_r1), Counter(tgt_r1)
    return {h for h in set(src_r1) | set(tgt_r1) if src_counts[h] != tgt_counts[h]}


def _recovered(res):
    return set(res.source_hashes) | set(res.target_hashes)


def _distinct(rng, count):
    seen: set[int] = set()
    while len(seen) < count:
        seen.add(rng.randint(0, _RH_MAX))
    return list(seen)


def _gen_clean_le2(rng):
    kind = rng.choice(["d1", "swap", "extras", "extras_repeat"])
    if kind == "d1":
        rh1, rh2 = rng.randint(0, _RH_MAX), rng.randint(0, _RH_MAX)
        return ([rh1], [rh2], [], []) if rng.random() < 0.5 else ([], [], [rh1], [rh2])
    if kind == "swap":
        pair = _distinct(rng, 2)
        return [pair[0]], [rng.randint(0, _RH_MAX)], [pair[1]], [rng.randint(0, _RH_MAX)]
    if kind == "extras":
        pair = _distinct(rng, 2)
        rh2s = [rng.randint(0, _RH_MAX), rng.randint(0, _RH_MAX)]
        return (pair, rh2s, [], []) if rng.random() < 0.5 else ([], [], pair, rh2s)
    rh1, rh2 = rng.randint(0, _RH_MAX), rng.randint(0, _RH_MAX)
    return [rh1, rh1], [rh2, rh2], [], []


def _gen_ge3(rng):
    count = rng.randint(3, 8)
    src_r1, src_r2, tgt_r1, tgt_r2 = [], [], [], []
    for _ in range(count):
        rh1, rh2 = rng.randint(0, _RH_MAX), rng.randint(0, _RH_MAX)
        if rng.random() < 0.5:
            src_r1.append(rh1)
            src_r2.append(rh2)
        else:
            tgt_r1.append(rh1)
            tgt_r2.append(rh2)
    return src_r1, src_r2, tgt_r1, tgt_r2


def test_clean_le2_configs_always_solve_with_exact_hashes():
    rng = random.Random(_SEED)
    for _ in range(_TRIALS):
        src_r1, src_r2, tgt_r1, tgt_r2 = _gen_clean_le2(rng)
        res = _solve(src_r1, src_r2, tgt_r1, tgt_r2)
        assert res is not None, f"clean <=2 bucket failed to solve: {(src_r1, tgt_r1)}"
        assert _recovered(res) == _diff_hashes(
            src_r1, tgt_r1
        ), f"recovered hashes do not match truth for {(src_r1, tgt_r1)}: {res}"


def test_solver_never_false_solves_including_beyond_capacity():
    rng = random.Random(_SEED + 1)
    generators = (_gen_clean_le2, _gen_ge3)
    for _ in range(_TRIALS):
        gen = rng.choice(generators)
        src_r1, src_r2, tgt_r1, tgt_r2 = gen(rng)
        res = _solve(src_r1, src_r2, tgt_r1, tgt_r2)
        if res is None:
            continue
        truth = _diff_hashes(src_r1, tgt_r1)
        assert _recovered(res) >= truth, (
            f"FALSE SOLVE: recovered {_recovered(res)} does not cover true diff {truth} "
            f"for src={src_r1} tgt={tgt_r1}"
        )


def test_cross_side_rh1_collision_declines_safely():
    r2_src, r2_tgt = 111, 222
    res = engine.solve_sub_bucket(
        0,
        d_cnt=0,
        d_p1=0,
        d_p2=0,
        d_p1_rh2=r2_src - r2_tgt,
        d_p2_rh2=r2_src * r2_src - r2_tgt * r2_tgt,
    )
    assert res is None


def _solve_rate_floor(sub_bucket_count: int) -> float:
    cap = min(engine.MAX_MISMATCHED_SUBBUCKETS_TO_SOLVE, engine.SYSTEMIC_GUARD_THRESHOLD * sub_bucket_count)
    lam_max = -math.log(1.0 - cap / sub_bucket_count)
    return math.exp(-lam_max) * (1.0 + lam_max)


def test_systemic_guard_enforces_solve_rate_floor_per_tier():
    tier_counts = {sub for (_max_rows, sub, _bucket) in SUB_BUCKET_TIERS}
    tier_counts.add(SUB_BUCKET_COUNT)
    for sub_bucket_count in sorted(tier_counts):
        floor = _solve_rate_floor(sub_bucket_count)
        assert floor >= _SOLVE_RATE_FLOOR, (
            f"tier N={sub_bucket_count}: solve-rate floor {floor:.4%} dropped below "
            f"{_SOLVE_RATE_FLOOR:.1%} - the systemic guard or tier table was loosened"
        )

    smallest = min(tier_counts)
    assert _solve_rate_floor(smallest) == min(_solve_rate_floor(n) for n in tier_counts)
