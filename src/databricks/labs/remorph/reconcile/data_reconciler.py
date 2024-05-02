from pyspark.sql import DataFrame
from pyspark.sql.functions import col, lit, when

from databricks.labs.remorph.reconcile.recon_config import ReconcileOutput


class DataReconciler:

    def compare_data(self, source: DataFrame, target: DataFrame, join_cols: list[str],
                     report_type: str) -> ReconcileOutput:
        join = join_cols if report_type in {"data", "all"} else "hash_value_recon"
        df = source.alias('s').join(other=target.alias('t'), on=join, how="full")

        mismatch = self._get_mismatch_data(df) if report_type in {"all", "data"} else None
        missing_in_src = (
            df.filter(col("s.hash_value_recon").isNull())
            .select((join_cols if report_type == "all" else "t.*"))
            .drop("hash_value_recon")
        )
        missing_in_tgt = (
            df.filter(col("t.hash_value_recon").isNull())
            .drop("hash_value_recon")
            .select((join_cols if report_type == "all" else "s.*"))
            .drop("hash_value_recon")
        )
        return ReconcileOutput(missing_in_src=missing_in_src, missing_in_tgt=missing_in_tgt, mismatch=mismatch)

    @staticmethod
    def _get_mismatch_data(df: DataFrame) -> DataFrame:
        return (
            df.filter((col("s.hash_value_recon").isNotNull()) & (col("t.hash_value_recon").isNotNull()))
            .withColumn("hash_match", col("s.hash_value_recon") == col("t.hash_value_recon"))
            .filter(col("hash_match") == lit(False))
            .select("s.*")
            .drop("hash_value_recon")
        )
