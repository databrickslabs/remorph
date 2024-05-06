from pyspark.sql import DataFrame
from pyspark.sql.functions import col, expr, lit

from databricks.labs.remorph.reconcile.constants import Constants
from databricks.labs.remorph.reconcile.recon_config import ReconcileOutput


def reconcile_data(source: DataFrame, target: DataFrame, join_columns: list[str], report_type: str) -> ReconcileOutput:
    source_alias = 'src'
    target_alias = 'tgt'
    if report_type not in {"data", "all"}:
        join_columns = Constants.hash_column_name
    df = source.alias(source_alias).join(other=target.alias(target_alias), on=join_columns, how="full")

    mismatch = _get_mismatch_data(df, source_alias, target_alias) if report_type in {"all", "data"} else None
    missing_in_src = (
        df.filter(col(f"{source_alias}.{Constants.hash_column_name}").isNull())
        .select((join_columns if report_type == "all" else f"{target_alias}.*"))
        .drop(Constants.hash_column_name)
    )
    missing_in_tgt = (
        df.filter(col(f"{target_alias}.{Constants.hash_column_name}").isNull())
        .select((join_columns if report_type == "all" else f"{source_alias}.*"))
        .drop(Constants.hash_column_name)
    )
    return ReconcileOutput(missing_in_src=missing_in_src, missing_in_tgt=missing_in_tgt, mismatch=mismatch)


def _get_mismatch_data(df: DataFrame, src_alias: str, tgt_alias: str) -> DataFrame:
    return (
        df.filter(
            (col(f"{src_alias}.{Constants.hash_column_name}").isNotNull())
            & (col(f"{tgt_alias}.{Constants.hash_column_name}").isNotNull())
        )
        .withColumn(
            "hash_match",
            col(f"{src_alias}.{Constants.hash_column_name}") == col(f"{tgt_alias}.{Constants.hash_column_name}"),
        )
        .filter(col("hash_match") == lit(False))
        .select(f"{src_alias}.*")
        .drop(Constants.hash_column_name)
    )


def capture_mismatch_data_and_columns(
    source: DataFrame, target: DataFrame, key_columns: list[str]
) -> (DataFrame, list[str]):
    source_columns = source.columns
    target_columns = target.columns

    if source_columns != target_columns:
        message = "source and target should have same columns for capturing the mismatch data"
        raise ValueError(message)

    check_columns = [ele for ele in source_columns if ele not in key_columns]
    mismatch_df = _get_mismatch_df(source, target, key_columns, check_columns)
    mismatch_columns = _get_mismatch_columns(mismatch_df, check_columns)
    return mismatch_df, mismatch_columns


def _get_mismatch_columns(df: DataFrame, columns: list[str]):
    mismatch_columns = []
    for column in columns:
        if df.where(~col(column + "_match")).take(1):
            mismatch_columns.append(column)
    return mismatch_columns


def _get_mismatch_df(source: DataFrame, target: DataFrame, join_columns: list[str], column_list: list[str]):
    source_aliased = [col('base.' + c).alias(c + '_base') for c in column_list]
    target_aliased = [col('compare.' + c).alias(c + '_compare') for c in column_list]

    match_expr = [expr(f"{c}_base=={c}_compare").alias(c + "_match") for c in column_list]
    select_expr = join_columns + source_aliased + target_aliased + match_expr

    filter_columns = " and ".join([c + "_match" for c in column_list])
    filter_expr = ~expr(filter_columns)

    mismatch_df = (
        source.alias('base')
        .join(other=target.alias('compare'), on=join_columns, how="inner")
        .select(select_expr)
        .filter(filter_expr)
    )
    compare_columns = [column for column in mismatch_df.columns if column not in join_columns]
    return mismatch_df.select(*join_columns + sorted(compare_columns))
