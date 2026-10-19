"""Shared constants and SQL helpers for fingerprint detection and row filtering."""

from __future__ import annotations

NULL_SENTINEL = "_null_recon_"

SEPARATOR_PYTHON = "\x01"
SEPARATOR_REDSHIFT_SQL = "CHR(1)"
SEPARATOR_SPARK_SQL = "CHAR(1)"


def quote_identifier(bare: str, quote_char: str) -> str:
    """Wrap ``bare`` in ``quote_char`` delimiters, doubling any embedded delimiter."""
    escaped = bare.replace(quote_char, quote_char * 2)
    return f"{quote_char}{escaped}{quote_char}"


SUB_BUCKET_COUNT = 1_048_576
BUCKET_COUNT = 32_768

SUB_BUCKET_TIERS: tuple[tuple[int | None, int, int], ...] = (
    (50_000, 16_384, 128),
    (500_000, 262_144, 512),
    (50_000_000, 1_048_576, 1_024),
    (500_000_000, 2_097_152, 2_048),
    (5_000_000_000, 4_194_304, 4_096),
    (50_000_000_000, 8_388_608, 8_192),
    (None, 16_777_216, 16_384),
)


def pick_sub_bucket_count(row_count: int | None) -> tuple[int, int]:
    """Select (sub_bucket_count, bucket_count) for ``row_count``."""
    if row_count is None or row_count <= 0:
        return SUB_BUCKET_COUNT, BUCKET_COUNT
    for max_row_count, sub_buckets, buckets in SUB_BUCKET_TIERS:
        if max_row_count is None or row_count <= max_row_count:
            return sub_buckets, buckets
    return SUB_BUCKET_COUNT, BUCKET_COUNT


def build_fingerprint_where_clause(
    sb_expr: str,
    rh1_expr: str,
    solved_hashes: dict[int, list[int]],
    unsolved_sb_ids: list[int],
) -> str:
    """Build the WHERE body (no ``WHERE``, no trailing alias) for a filtered fetch."""
    if not solved_hashes and not unsolved_sb_ids:
        raise ValueError(
            "build_fingerprint_where_clause requires at least one of solved_hashes "
            "or unsolved_sb_ids to be non-empty; the empty case must be filtered "
            "out by the caller before issuing a fetch."
        )
    conditions: list[str] = []
    if solved_hashes:
        sb_list = ", ".join(str(sb_id) for sb_id in sorted(solved_hashes))
        hash_list = ", ".join(str(h) for h in sorted({h for hs in solved_hashes.values() for h in hs}))
        conditions.append(f"({sb_expr} IN ({sb_list}) AND {rh1_expr} IN ({hash_list}))")
    if unsolved_sb_ids:
        sb_list = ", ".join(str(sb_id) for sb_id in sorted(unsolved_sb_ids))
        conditions.append(f"{sb_expr} IN ({sb_list})")
    return " OR ".join(conditions)
