import logging
import math
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Literal

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

DetectionVerdict = Literal["MATCH", "MISMATCH"]

logger = logging.getLogger(__name__)

SYSTEMIC_GUARD_THRESHOLD = 0.15
SYSTEMIC_GUARD_MIN_MISMATCH_COUNT = 50
MAX_MISMATCHED_SUBBUCKETS_TO_SOLVE = 50_000
MAX_RH_VALUE = 0xFFFFFFFF


@dataclass
class SolveResult:
    sub_bucket_id: int
    source_hashes: list[int]
    target_hashes: list[int]


@dataclass
class DetectionResult:
    verdict: DetectionVerdict
    solved_results: list[SolveResult] = field(default_factory=list)
    unsolved_sb_ids: list[int] = field(default_factory=list)
    total_mismatched_sbs: int = 0
    systemic_mismatch: bool = False


@contextmanager
def _cached_frame(df: DataFrame) -> Iterator[DataFrame]:
    """Yield a cached ``df`` and guarantee ``unpersist`` on exit."""
    try:
        yield df
    finally:
        df.unpersist()


def detect_and_solve(
    source_agg_df: DataFrame,
    target_agg_df: DataFrame,
) -> DetectionResult:
    """Compare source and target sub-bucket aggregates and solve for culprit hashes."""
    joined = (
        source_agg_df.alias("src")
        .join(
            target_agg_df.alias("tgt"),
            on=["sub_bucket_id"],
            how="full",
        )
        .select(
            F.coalesce(F.col("src.sub_bucket_id"), F.col("tgt.sub_bucket_id")).alias("sub_bucket_id"),
            F.coalesce(F.col("src.cnt"), F.lit(0)).alias("src_cnt"),
            F.coalesce(F.col("tgt.cnt"), F.lit(0)).alias("tgt_cnt"),
            F.coalesce(F.col("src.p1"), F.lit(0)).alias("src_p1"),
            F.coalesce(F.col("tgt.p1"), F.lit(0)).alias("tgt_p1"),
            F.coalesce(F.col("src.p2"), F.lit(0)).alias("src_p2"),
            F.coalesce(F.col("tgt.p2"), F.lit(0)).alias("tgt_p2"),
            F.coalesce(F.col("src.p1_rh2"), F.lit(0)).alias("src_p1_rh2"),
            F.coalesce(F.col("tgt.p1_rh2"), F.lit(0)).alias("tgt_p1_rh2"),
            F.coalesce(F.col("src.p2_rh2"), F.lit(0)).alias("src_p2_rh2"),
            F.coalesce(F.col("tgt.p2_rh2"), F.lit(0)).alias("tgt_p2_rh2"),
        )
    ).cache()

    with _cached_frame(joined):
        mismatch_condition = (
            (F.col("src_cnt") != F.col("tgt_cnt"))
            | (F.col("src_p1") != F.col("tgt_p1"))
            | (F.col("src_p2") != F.col("tgt_p2"))
            | (F.col("src_p1_rh2") != F.col("tgt_p1_rh2"))
            | (F.col("src_p2_rh2") != F.col("tgt_p2_rh2"))
        )
        mismatched = joined.filter(mismatch_condition)

        counts_row = joined.agg(
            F.count("*").alias("total_sbs"),
            F.sum(F.when(mismatch_condition, F.lit(1)).otherwise(F.lit(0)).cast("long")).alias("mismatch_count"),
        ).collect()[0]
        total_sbs = int(counts_row["total_sbs"] or 0)
        mismatch_count = int(counts_row["mismatch_count"] or 0)

        if mismatch_count == 0:
            logger.info("Fingerprint detection: MATCH — all sub-buckets identical")
            return DetectionResult(verdict="MATCH")

        mismatch_ratio = mismatch_count / max(total_sbs, 1)
        logger.info(
            f"Fingerprint detection: {mismatch_count}/{total_sbs} sub-buckets mismatched ({mismatch_ratio * 100:.1f}%)"
        )

        is_systemic_ratio = (
            mismatch_ratio > SYSTEMIC_GUARD_THRESHOLD and mismatch_count >= SYSTEMIC_GUARD_MIN_MISMATCH_COUNT
        )
        if is_systemic_ratio or mismatch_count > MAX_MISMATCHED_SUBBUCKETS_TO_SOLVE:
            logger.warning(
                f"Fingerprint: systemic mismatch ({mismatch_ratio * 100:.1f}% > "
                f"{SYSTEMIC_GUARD_THRESHOLD * 100:.0f}% with {mismatch_count} >= "
                f"{SYSTEMIC_GUARD_MIN_MISMATCH_COUNT}, or {mismatch_count} > "
                f"{MAX_MISMATCHED_SUBBUCKETS_TO_SOLVE}) — falling through"
            )
            return DetectionResult(
                verdict="MISMATCH",
                total_mismatched_sbs=mismatch_count,
                systemic_mismatch=True,
            )

        mismatched_rows = mismatched.collect()

        solved_results: list[SolveResult] = []
        unsolved_sb_ids: list[int] = []

        for row in mismatched_rows:
            sb_id = int(row["sub_bucket_id"])
            d_cnt = int(row["src_cnt"]) - int(row["tgt_cnt"])
            d_p1 = int(row["src_p1"]) - int(row["tgt_p1"])
            d_p2 = int(row["src_p2"]) - int(row["tgt_p2"])
            d_p1_rh2 = int(row["src_p1_rh2"]) - int(row["tgt_p1_rh2"])
            d_p2_rh2 = int(row["src_p2_rh2"]) - int(row["tgt_p2_rh2"])

            result = solve_sub_bucket(sb_id, d_cnt, d_p1, d_p2, d_p1_rh2, d_p2_rh2)
            if result is not None:
                solved_results.append(result)
            else:
                unsolved_sb_ids.append(sb_id)

        logger.info(
            f"Fingerprint solver: {len(solved_results)} solved, "
            f"{len(unsolved_sb_ids)} unsolved out of {len(mismatched_rows)} mismatched sub-buckets"
        )

        return DetectionResult(
            verdict="MISMATCH",
            solved_results=solved_results,
            unsolved_sb_ids=unsolved_sb_ids,
            total_mismatched_sbs=mismatch_count,
        )


def solve_sub_bucket(
    sb_id: int,
    d_cnt: int,
    d_p1: int,
    d_p2: int,
    d_p1_rh2: int,
    d_p2_rh2: int,
) -> SolveResult | None:
    """Solve d=1 / d=2 cases for one mismatched sub-bucket; return None when unsolvable."""
    abs_d = abs(d_cnt)
    if abs_d == 1:
        return solve_d1(sb_id, d_cnt, d_p1, d_p2, d_p1_rh2, d_p2_rh2)
    if abs_d == 0 and d_p1 != 0:
        return solve_d2_swap(sb_id, d_p1, d_p2, d_p1_rh2, d_p2_rh2)
    if abs_d == 2:
        return _solve_d2_extras(sb_id, d_cnt, d_p1, d_p2, d_p1_rh2, d_p2_rh2)
    return None


def solve_d1(sb_id: int, d_cnt: int, d_p1: int, d_p2: int, d_p1_rh2: int, d_p2_rh2: int) -> SolveResult | None:
    """Solve d=1: one extra row on one side."""
    rh1 = abs(d_p1)

    if d_p2 != rh1 * rh1 * d_cnt:
        return None
    if rh1 > MAX_RH_VALUE:
        return None

    rh2 = abs(d_p1_rh2)
    if d_p2_rh2 != rh2 * rh2 * d_cnt:
        return None
    if rh2 > MAX_RH_VALUE:
        return None

    if d_cnt > 0:
        return SolveResult(sub_bucket_id=sb_id, source_hashes=[rh1], target_hashes=[])
    return SolveResult(sub_bucket_id=sb_id, source_hashes=[], target_hashes=[rh1])


def solve_d2_swap(
    sb_id: int,
    d_p1: int,
    d_p2: int,
    d_p1_rh2: int,
    d_p2_rh2: int,
) -> SolveResult | None:
    """Solve d=2 swap: same row count, one row's content changed."""
    if d_p1 == 0:
        return None
    if d_p2 % d_p1 != 0:
        return None

    h_sum = d_p2 // d_p1
    if (d_p1 + h_sum) % 2 != 0:
        return None
    h_old = (d_p1 + h_sum) // 2
    h_new = h_sum - h_old

    if h_old - h_new != d_p1 or h_old * h_old - h_new * h_new != d_p2:
        return None
    if not (0 <= h_old <= MAX_RH_VALUE and 0 <= h_new <= MAX_RH_VALUE):
        return None
    if not _cross_verify_d2_swap(d_p1_rh2, d_p2_rh2):
        return None

    return SolveResult(sub_bucket_id=sb_id, source_hashes=[h_old], target_hashes=[h_new])


def _solve_d2_extras(
    sb_id: int,
    d_cnt: int,
    d_p1: int,
    d_p2: int,
    d_p1_rh2: int,
    d_p2_rh2: int,
) -> SolveResult | None:
    """Solve d=2 extras: two extra rows on one side."""
    sign = 1 if d_cnt > 0 else -1
    sum_h = d_p1 * sign
    sum_sq = d_p2 * sign

    if sum_sq < 0:
        return None

    product_2 = sum_h * sum_h - sum_sq
    if product_2 < 0 or product_2 % 2 != 0:
        return None
    product = product_2 // 2

    discriminant = sum_h * sum_h - 4 * product
    if discriminant < 0:
        return None

    sqrt_disc = _isqrt(discriminant)
    if sqrt_disc is None:
        return None
    if (sum_h + sqrt_disc) % 2 != 0:
        return None

    hash_a = (sum_h + sqrt_disc) // 2
    hash_b = sum_h - hash_a

    if hash_a + hash_b != sum_h or hash_a * hash_a + hash_b * hash_b != sum_sq:
        return None
    if not (0 <= hash_a <= MAX_RH_VALUE and 0 <= hash_b <= MAX_RH_VALUE):
        return None
    if not _cross_verify_d2_extras(d_cnt, d_p1_rh2, d_p2_rh2):
        return None

    hashes = [hash_a] if hash_a == hash_b else sorted([hash_a, hash_b])
    if d_cnt > 0:
        return SolveResult(sub_bucket_id=sb_id, source_hashes=hashes, target_hashes=[])
    return SolveResult(sub_bucket_id=sb_id, source_hashes=[], target_hashes=hashes)


def _cross_verify_d2_swap(d_p1_rh2: int, d_p2_rh2: int) -> bool:
    """Independently solve the d=2 swap on the rh2 channel and confirm valid roots."""
    if d_p1_rh2 == 0:
        return d_p2_rh2 == 0
    if d_p2_rh2 % d_p1_rh2 != 0:
        return False
    h_sum = d_p2_rh2 // d_p1_rh2
    if (d_p1_rh2 + h_sum) % 2 != 0:
        return False
    h_old = (d_p1_rh2 + h_sum) // 2
    h_new = h_sum - h_old
    if h_old - h_new != d_p1_rh2:
        return False
    return 0 <= h_old <= MAX_RH_VALUE and 0 <= h_new <= MAX_RH_VALUE


def _cross_verify_d2_extras(d_cnt: int, d_p1_rh2: int, d_p2_rh2: int) -> bool:
    """Independently solve the d=2 extras quadratic on the rh2 channel."""
    sign = 1 if d_cnt > 0 else -1
    sum_h = d_p1_rh2 * sign
    sum_sq = d_p2_rh2 * sign
    if sum_sq < 0:
        return False
    product_2 = sum_h * sum_h - sum_sq
    if product_2 < 0 or product_2 % 2 != 0:
        return False
    discriminant = sum_h * sum_h - 4 * (product_2 // 2)
    if discriminant < 0:
        return False
    sqrt_disc = _isqrt(discriminant)
    if sqrt_disc is None:
        return False
    if (sum_h + sqrt_disc) % 2 != 0:
        return False
    h_a = (sum_h + sqrt_disc) // 2
    h_b = sum_h - h_a
    return 0 <= h_a <= MAX_RH_VALUE and 0 <= h_b <= MAX_RH_VALUE


def _isqrt(value: int) -> int | None:
    """Return the integer square root if ``value`` is a perfect square, else None."""
    if value < 0:
        return None
    root = math.isqrt(value)
    return root if root * root == value else None
