"""Spark-side detection (Stage-1) and Stage-2 filter helpers for the target Delta table."""

import logging

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import DecimalType, LongType

from databricks.labs.lakebridge.reconcile.connectors.dialect_utils import DialectUtils
from databricks.labs.lakebridge.reconcile.fingerprint.columns import counterpart_type_of
from databricks.labs.lakebridge.reconcile.fingerprint.constants import (
    SEPARATOR_PYTHON,
    SEPARATOR_SPARK_SQL,
    build_fingerprint_where_clause,
    quote_identifier,
)
from databricks.labs.lakebridge.reconcile.query_builder.column_transformer import serialize_column_for_hash
from databricks.labs.lakebridge.reconcile.recon_config import Schema

RH_OPERAND_TYPE = DecimalType(19, 0)
AGG_TYPE = DecimalType(38, 0)

logger = logging.getLogger(__name__)


def compute_target_fingerprint(
    spark: SparkSession,
    catalog: str | None,
    schema: str,
    table: str,
    columns: list[Schema],
    column_mapping: dict[str, str] | None,
    sub_bucket_count: int,
) -> DataFrame:
    """Compute Stage-1 sub-bucket aggregates on the target Delta table."""
    df = spark.table(_table_fqn(catalog, schema, table))

    concat_col = _build_concat_column(columns, column_mapping)
    md5_col = F.md5(concat_col)

    rh1_col = _hex_substr_to_long(md5_col, 1, 8)
    rh2_col = _hex_substr_to_long(md5_col, 9, 8)

    df_hashed = df.select(
        F.abs(rh1_col % F.lit(sub_bucket_count)).alias("sub_bucket_id"),
        rh1_col.alias("rh1"),
        rh2_col.alias("rh2"),
    )
    return df_hashed.groupBy("sub_bucket_id").agg(*_hash_agg_exprs())


def build_target_filter_subquery(
    catalog: str | None,
    schema: str,
    table: str,
    columns: list[Schema],
    column_mapping: dict[str, str] | None,
    solved_hashes: dict[int, list[int]],
    unsolved_sb_ids: list[int],
    *,
    sub_bucket_count: int,
) -> str:
    """Build the Spark-SQL subquery that filters target rows for Stage-2 surgical fetch."""
    concat_expr = _build_target_concat_sql(columns, column_mapping)
    rh1_expr = f"CAST(CONV(SUBSTR(MD5({concat_expr}), 1, 8), 16, 10) AS BIGINT)"
    sb_expr = f"ABS(MOD({rh1_expr}, {sub_bucket_count}))"
    where_clause = build_fingerprint_where_clause(sb_expr, rh1_expr, solved_hashes, unsolved_sb_ids)
    return f"(SELECT * FROM {_table_fqn(catalog, schema, table)} WHERE {where_clause}) _fp_filtered"


def _build_concat_column(
    columns: list[Schema],
    column_mapping: dict[str, str] | None,
) -> F.Column:
    """Concatenate serialised target columns into a single Column for MD5 hashing."""
    parts = [
        F.expr(serialize_target_column_sql(_target_col_name(c, column_mapping), c.data_type, counterpart_type_of(c)))
        for c in columns
    ]
    if len(parts) == 1:
        return parts[0]
    result = parts[0]
    for part in parts[1:]:
        result = F.concat(result, F.lit(SEPARATOR_PYTHON), part)
    return result


def _build_target_concat_sql(
    columns: list[Schema],
    column_mapping: dict[str, str] | None,
) -> str:
    """SQL-string sibling of ``_build_concat_column`` for the Stage-2 filter subquery."""
    col_exprs = [
        serialize_target_column_sql(_target_col_name(c, column_mapping), c.data_type, counterpart_type_of(c))
        for c in columns
    ]
    if len(col_exprs) == 1:
        return col_exprs[0]
    sep_parts: list[str] = []
    for i, expr in enumerate(col_exprs):
        if i > 0:
            sep_parts.append(SEPARATOR_SPARK_SQL)
        sep_parts.append(expr)
    return f"CONCAT({', '.join(sep_parts)})"


_SPARK_IDENTIFIER_QUOTE = "`"


def quote_spark_identifier(bare: str) -> str:
    """Wrap ``bare`` in Spark SQL's backtick identifier delimiters (see
    ``constants.quote_identifier`` for the escaping + case-preservation rationale)."""
    return quote_identifier(bare, _SPARK_IDENTIFIER_QUOTE)


def serialize_target_column_sql(col_name: str, col_type: str, counterpart_type: str | None = None) -> str:
    """Per-column target serializer (Databricks SQL string)."""
    quoted = quote_spark_identifier(col_name)
    return serialize_column_for_hash(quoted, col_type, counterpart_type, "target")


def _target_col_name(schema_col: Schema, column_mapping: dict[str, str] | None) -> str:
    """Resolve target physical column name; ``Schema.ansi_normalized_column_name`` arrives ANSI-delimited."""
    bare = DialectUtils.unnormalize_identifier(schema_col.ansi_normalized_column_name)
    if column_mapping:
        return column_mapping.get(bare.lower(), bare)
    return bare


def _table_fqn(catalog: str | None, schema: str, table: str) -> str:
    """Catalog / schema / table come from ReconcileConfig and are validated
    upstream (Unity Catalog enforces a strict identifier grammar), but routing
    through ``quote_spark_identifier`` makes the FQN robust against names
    containing ``-``, ``.``, or other characters Spark would otherwise treat
    specially. Defensive parity with column-name quoting on this same boundary.
    """
    parts = [quote_spark_identifier(schema), quote_spark_identifier(table)]
    if catalog:
        parts.insert(0, quote_spark_identifier(catalog))
    return ".".join(parts)


def _hash_agg_exprs() -> list[F.Column]:
    rh1_dec19 = F.col("rh1").cast(RH_OPERAND_TYPE)
    rh2_dec19 = F.col("rh2").cast(RH_OPERAND_TYPE)
    rh1_dec38 = F.col("rh1").cast(AGG_TYPE)
    rh2_dec38 = F.col("rh2").cast(AGG_TYPE)
    return [
        F.count("*").alias("cnt"),
        F.sum(rh1_dec38).alias("p1"),
        F.sum(rh1_dec19 * rh1_dec19).alias("p2"),
        F.sum(rh2_dec38).alias("p1_rh2"),
        F.sum(rh2_dec19 * rh2_dec19).alias("p2_rh2"),
    ]


def _hex_substr_to_long(md5_col: F.Column, start: int, length: int) -> F.Column:
    """Convert an MD5 hex substring to a long via Photon-safe ASCII arithmetic."""
    hex_slice = F.substring(md5_col, start, length)
    ascii_0 = F.ascii(F.lit("0"))
    ascii_a = F.ascii(F.lit("a"))
    result = F.lit(0).cast(LongType())
    for i in range(length):
        char_col = F.substring(hex_slice, i + 1, 1)
        digit = (
            F.when(F.ascii(char_col) >= ascii_a, F.ascii(char_col) - ascii_a + F.lit(10))
            .otherwise(F.ascii(char_col) - ascii_0)
            .cast(LongType())
        )
        result = result * F.lit(16).cast(LongType()) + digit
    return result
