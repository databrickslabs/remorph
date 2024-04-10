from pyspark.sql import DataFrame
from pyspark.sql.functions import col, lit, when

from databricks.labs.remorph.reconcile.recon_config import ReconcileOutput


class Comparator:

    def compare_data(self, source: DataFrame, target: DataFrame, join_cols: list[str], report: str) -> ReconcileOutput:
        join = join_cols if report in ("all", "data") else "hash_value__recon"
        df = source.alias('s').join(target.alias("t"), join, how='full')

        mismatch = self._get_mismatch_data(df) if report in ("all", "data") else None
        missing_in_src = (
            df.filter(col("s.hash_value__recon").isNull())
            .select((join_cols if report == "all" else "t.*"))
            .drop("hash_value__recon")
        )
        missing_in_tgt = (
            df.filter(col("t.hash_value__recon").isNull())
            .drop("hash_value__recon")
            .select((join_cols if report == "all" else "s.*"))
            .drop("hash_value__recon")
        )
        return ReconcileOutput(missing_in_src=missing_in_src, missing_in_tgt=missing_in_tgt, mismatch=mismatch)

    @staticmethod
    def _get_mismatch_data(df: DataFrame) -> DataFrame:
        return (
            df.filter((col("s.hash_value__recon").isNotNull()) & (col("t.hash_value__recon").isNotNull()))
            .withColumn(
                "hash_match",
                when(col("s.hash_value__recon") == col("t.hash_value__recon"), lit(True)).otherwise(lit(False)),
            )
            .filter(col("hash_match") == lit(False))
            .select("s.*")
            .drop("hash_value__recon")
        )
