"""Redshift SQL generation for fingerprint detection and surgical row fetch."""

import logging

from databricks.labs.lakebridge.reconcile.connectors.dialect_utils import DialectUtils
from databricks.labs.lakebridge.reconcile.fingerprint.columns import counterpart_type_of
from databricks.labs.lakebridge.reconcile.fingerprint.constants import (
    SEPARATOR_REDSHIFT_SQL,
    build_fingerprint_where_clause,
    quote_identifier,
)
from databricks.labs.lakebridge.reconcile.fingerprint.query_builders.base import FingerprintQueryBuilder
from databricks.labs.lakebridge.reconcile.query_builder.column_transformer import serialize_column_for_hash
from databricks.labs.lakebridge.reconcile.recon_config import Schema

logger = logging.getLogger(__name__)


_REDSHIFT_IDENTIFIER_QUOTE = '"'


def quote_redshift_identifier(bare: str) -> str:
    """Wrap ``bare`` in Redshift's ``"..."`` identifier delimiters (see
    ``constants.quote_identifier`` for the escaping + case-preservation rationale)."""
    return quote_identifier(bare, _REDSHIFT_IDENTIFIER_QUOTE)


class RedshiftFingerprintQueryBuilder(FingerprintQueryBuilder):
    """Generate Redshift SQL for fingerprint detection and surgical row fetch."""

    def serialize_column(self, col_name: str, col_type: str, counterpart_type: str | None = None) -> str:
        bare = DialectUtils.unnormalize_identifier(col_name)
        quoted = quote_redshift_identifier(bare)
        return serialize_column_for_hash(quoted, col_type, counterpart_type, "source")

    def build_detection_sql(
        self,
        schema: str,
        table: str,
        columns: list[Schema],
        column_mapping: dict[str, str] | None,
        sub_bucket_count: int,
    ) -> str:
        rh1_expr, rh2_expr, sb_expr = self._md5_hash_exprs(columns, sub_bucket_count)

        rh1_dec19 = f"CAST({rh1_expr} AS DECIMAL(19,0))"
        rh1_dec38 = f"CAST({rh1_expr} AS DECIMAL(38,0))"
        rh2_dec19 = f"CAST({rh2_expr} AS DECIMAL(19,0))"
        rh2_dec38 = f"CAST({rh2_expr} AS DECIMAL(38,0))"

        from_table = f"{quote_redshift_identifier(schema)}.{quote_redshift_identifier(table)}"
        return (
            f"SELECT {sb_expr} AS sub_bucket_id, "
            f"COUNT(*) AS cnt, "
            f"SUM({rh1_dec38}) AS p1, "
            f"SUM({rh1_dec19} * {rh1_dec19}) AS p2, "
            f"SUM({rh2_dec38}) AS p1_rh2, "
            f"SUM({rh2_dec19} * {rh2_dec19}) AS p2_rh2 "
            f"FROM {from_table} "
            f"GROUP BY sub_bucket_id"
        )

    def build_source_filter_subquery(
        self,
        schema: str,
        table: str,
        columns: list[Schema],
        sub_bucket_count: int,
        solved_hashes: dict[int, list[int]],
        unsolved_sb_ids: list[int],
    ) -> str:
        rh1_expr, _, sb_expr = self._md5_hash_exprs(columns, sub_bucket_count)
        where_clause = build_fingerprint_where_clause(sb_expr, rh1_expr, solved_hashes, unsolved_sb_ids)
        from_table = f"{quote_redshift_identifier(schema)}.{quote_redshift_identifier(table)}"
        return f"(SELECT * FROM {from_table} WHERE {where_clause}) _fp_filtered"

    def build_concat_expression(self, columns: list[Schema]) -> str:
        """Concat over source physical column names for MD5."""
        parts = [
            self.serialize_column(c.ansi_normalized_column_name, c.data_type, counterpart_type_of(c)) for c in columns
        ]
        return f" || {SEPARATOR_REDSHIFT_SQL} || ".join(parts)

    def _md5_hash_exprs(self, columns: list[Schema], sub_bucket_count: int) -> tuple[str, str, str]:
        """Return the (rh1, rh2, sb_expr) MD5-derived SQL fragments shared by detection + filter SQL."""
        concat_expr = self.build_concat_expression(columns)
        rh1_expr = f"STRTOL(SUBSTRING(MD5({concat_expr}), 1, 8), 16)"
        rh2_expr = f"STRTOL(SUBSTRING(MD5({concat_expr}), 9, 8), 16)"
        sb_expr = f"ABS(MOD({rh1_expr}, {sub_bucket_count}))"
        return rh1_expr, rh2_expr, sb_expr
