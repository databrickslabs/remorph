"""Target row-count fetcher for adaptive sub-bucket tier selection."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum

from pyspark.sql import SparkSession
from pyspark.sql.utils import AnalysisException

from databricks.labs.lakebridge.reconcile.fingerprint.constants import quote_identifier

_SPARK_IDENTIFIER_QUOTE = "`"

logger = logging.getLogger(__name__)


class RowCountSource(str, Enum):
    """Provenance of the row count used for tier selection."""

    DELTA_DESCRIBE_DETAIL = "delta_describe_detail"
    COUNT_STAR = "count_star"
    STATIC_DEFAULT = "static_default"


@dataclass(frozen=True)
class RowCountResult:
    """``row_count`` is None only when ``source == STATIC_DEFAULT``."""

    row_count: int | None
    source: RowCountSource


def fetch_target_row_count(
    spark: SparkSession,
    *,
    catalog: str | None,
    schema: str,
    table: str,
) -> RowCountResult:
    """Resolve the target row count via cheap, metadata-first paths."""
    fully_qualified = _build_fqn(catalog=catalog, schema=schema, table=table)

    delta_count = _try_describe_detail(spark, fully_qualified)
    if delta_count is not None:
        logger.info(
            f"fingerprint.tier.row_count_source=delta_describe_detail "
            f"table={fully_qualified} row_count={delta_count}"
        )
        return RowCountResult(row_count=delta_count, source=RowCountSource.DELTA_DESCRIBE_DETAIL)

    count_star = _try_count_star(spark, fully_qualified)
    if count_star is not None:
        logger.info(f"fingerprint.tier.row_count_source=count_star table={fully_qualified} row_count={count_star}")
        return RowCountResult(row_count=count_star, source=RowCountSource.COUNT_STAR)

    logger.warning(
        f"fingerprint.tier.row_count_source=static_default table={fully_qualified} — DESCRIBE DETAIL "
        "exposed no numRecords and SELECT COUNT(*) was unavailable (target may be non-Delta, "
        "missing, or unreadable); falling back to the default tier."
    )
    return RowCountResult(row_count=None, source=RowCountSource.STATIC_DEFAULT)


def _build_fqn(*, catalog: str | None, schema: str, table: str) -> str:
    """Backtick-quote each identifier so a delimiting-needed name (hyphen, reserved word,
    embedded dot) cannot malform the ``DESCRIBE DETAIL`` SQL. Parity with
    ``spark_target._table_fqn``; without it such a name makes DESCRIBE DETAIL fail, the
    error is swallowed here, and tier selection silently degrades to the static default.
    """
    parts = [
        quote_identifier(schema, _SPARK_IDENTIFIER_QUOTE),
        quote_identifier(table, _SPARK_IDENTIFIER_QUOTE),
    ]
    if catalog:
        parts.insert(0, quote_identifier(catalog, _SPARK_IDENTIFIER_QUOTE))
    return ".".join(parts)


def _try_describe_detail(spark: SparkSession, fully_qualified_name: str) -> int | None:
    """Run DESCRIBE DETAIL and return numRecords when available."""
    try:
        detail_df = spark.sql(f"DESCRIBE DETAIL {fully_qualified_name}")
        if "numRecords" not in detail_df.columns:
            logger.debug(f"DESCRIBE DETAIL on {fully_qualified_name} returned no numRecords column")
            return None
        rows = detail_df.select("numRecords").collect()
    except AnalysisException as exc:
        logger.debug(f"DESCRIBE DETAIL failed for {fully_qualified_name}: {exc}")
        return None
    except (KeyboardInterrupt, SystemExit, GeneratorExit):
        raise
    except BaseException as exc:
        logger.debug(f"DESCRIBE DETAIL raised unexpected error for {fully_qualified_name}: {exc}")
        return None

    if not rows:
        logger.debug(f"DESCRIBE DETAIL on {fully_qualified_name} returned 0 rows")
        return None

    num_records = rows[0]["numRecords"]
    if num_records is None:
        logger.debug(f"DESCRIBE DETAIL on {fully_qualified_name} returned NULL numRecords")
        return None

    if not isinstance(num_records, int) or num_records < 0:
        logger.debug(f"DESCRIBE DETAIL on {fully_qualified_name} returned unexpected numRecords value {num_records!r}")
        return None

    return num_records


def _try_count_star(spark: SparkSession, fully_qualified_name: str) -> int | None:
    """Run ``SELECT COUNT(*)`` and return the count, or None on any failure (never raises)."""
    try:
        rows = spark.sql(f"SELECT COUNT(*) AS cnt FROM {fully_qualified_name}").collect()
    except AnalysisException as exc:
        logger.debug(f"SELECT COUNT(*) failed for {fully_qualified_name}: {exc}")
        return None
    except (KeyboardInterrupt, SystemExit, GeneratorExit):
        raise
    except BaseException as exc:
        logger.debug(f"SELECT COUNT(*) raised unexpected error for {fully_qualified_name}: {exc}")
        return None

    if not rows:
        logger.debug(f"SELECT COUNT(*) on {fully_qualified_name} returned 0 rows")
        return None

    count = rows[0]["cnt"]
    if count is None:
        logger.debug(f"SELECT COUNT(*) on {fully_qualified_name} returned NULL")
        return None

    if not isinstance(count, int) or count < 0:
        logger.debug(f"SELECT COUNT(*) on {fully_qualified_name} returned unexpected value {count!r}")
        return None

    return count
