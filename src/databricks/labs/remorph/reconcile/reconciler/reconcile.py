from pyspark.sql import DataFrame
from pyspark.sql.functions import col, lit, when

from databricks.labs.remorph.reconcile.recon_config import ReconcileOutput


class Reconcile:

    def reconcile_data(self, source: DataFrame, target: DataFrame, join_cols: list[str],
                       report: str) -> ReconcileOutput:
        join = join_cols if report == "all" else "hash_id"
        df = (source.alias('s').join(target.alias("t"), join, how='full'))

        mismatch = self._get_mismatch_data(df) if report == 'all' else None
        missing_in_src = (df.filter(col("s.hash_id").isNull()).select(*join))
        missing_in_tgt = (df.filter(col("t.hash_id").isNull()).select(*join))
        return ReconcileOutput(
            missing_in_src=missing_in_src,
            missing_in_tgt=missing_in_tgt,
            mismatch=mismatch
        )

    @staticmethod
    def _get_mismatch_data(df: DataFrame) -> DataFrame:
        return (df.filter((col("s.hash_id").isNotNull()) & (col("t.hash_id").isNotNull()))
                .withColumn("hash_match",
                            when(col("s.hash_id") == col("t.hash_id"), lit(True)).otherwise(lit(False)))
                .filter(col("hash_match") == lit(False)))
