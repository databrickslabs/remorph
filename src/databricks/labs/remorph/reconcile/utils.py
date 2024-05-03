from pyspark.sql import DataFrame
from pyspark.sql.functions import col, expr, lit

from databricks.labs.remorph.reconcile.recon_config import ReconcileOutput


def reconcile_data(source: DataFrame, target: DataFrame, join_cols: list[str], report_type: str) -> ReconcileOutput:
    source_alias = 'src'
    target_alias = 'tgt'
    join = join_cols if report_type in {"data", "all"} else "hash_value_recon"
    df = source.alias(source_alias).join(other=target.alias(target_alias), on=join, how="full")

    mismatch = _get_mismatch_data(df, source_alias, target_alias) if report_type in {"all", "data"} else None
    missing_in_src = (
        df.filter(col(f"{source_alias}.hash_value_recon").isNull())
        .select((join_cols if report_type == "all" else f"{target_alias}.*"))
        .drop("hash_value_recon")
    )
    missing_in_tgt = (
        df.filter(col(f"{target_alias}.hash_value_recon").isNull())
        .select((join_cols if report_type == "all" else f"{source_alias}.*"))
        .drop("hash_value_recon")
    )
    return ReconcileOutput(missing_in_src=missing_in_src, missing_in_tgt=missing_in_tgt, mismatch=mismatch)


def _get_mismatch_data(df: DataFrame, src_alias: str, tgt_alias: str) -> DataFrame:
    return (
        df.filter(
            (col(f"{src_alias}.hash_value_recon").isNotNull()) & (col(f"{tgt_alias}.hash_value_recon").isNotNull())
        )
        .withColumn("hash_match", col(f"{src_alias}.hash_value_recon") == col(f"{tgt_alias}.hash_value_recon"))
        .filter(col("hash_match") == lit(False))
        .select(f"{src_alias}.*")
        .drop("hash_value_recon")
    )


def capture_mismatch_data_and_cols(
    source: DataFrame, target: DataFrame, join_cols: list[str]
) -> (DataFrame, list[str]):
    source_cols = source.columns
    target_cols = target.columns

    assert source_cols == target_cols, "source and target should have same columns for capturing the mismatch data"

    check_cols = [ele for ele in source_cols if ele not in join_cols]
    mismatch_df = _get_mismatch_df(source, target, join_cols, check_cols)
    mismatch_cols = _get_mismatch_cols(mismatch_df, check_cols)
    return mismatch_df, mismatch_cols


def _get_mismatch_cols(df: DataFrame, cols: list[str]):
    mismatch_cols = []
    for column in cols:
        if df.where(~col(column + "_match")).take(1):
            mismatch_cols.append(column)
    return mismatch_cols


def _get_mismatch_df(source: DataFrame, target: DataFrame, join_cols: list[str], check_cols: list[str]):
    source_aliased = [col('base.' + c).alias(c + '_base') for c in check_cols]
    target_aliased = [col('compare.' + c).alias(c + '_compare') for c in check_cols]

    match_expr = [expr(f"{c}_base=={c}_compare").alias(c + "_match") for c in check_cols]
    select_expr = join_cols + source_aliased + target_aliased + match_expr

    filter_cols = " and ".join([c + "_match" for c in check_cols])
    filter_expr = ~expr(filter_cols)

    res_df = source.alias('base').join(target.alias('compare'), join_cols).select(select_expr).filter(filter_expr)
    compare_cols = [ele for ele in res_df.columns if ele not in join_cols]
    return res_df.select(*join_cols + sorted(compare_cols))
