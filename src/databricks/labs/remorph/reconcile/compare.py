from pyspark.sql import DataFrame
from pyspark.sql.functions import col, expr, lit

from databricks.labs.remorph.reconcile.constants import Constants
from databricks.labs.remorph.reconcile.exception import ColumnMismatchException
from databricks.labs.remorph.reconcile.recon_config import (
    MismatchOutput,
    ReconcileOutput,
)


def raise_column_mismatch_exception(msg: str, source_missing: list[str], target_missing: list[str]) -> Exception:
    error_msg = (
        f"{msg}\n"
        f"columns missing in source: {','.join(source_missing) if source_missing else None}\n"
        f"columns missing in target: {','.join(target_missing) if target_missing else None}\n"
    )
    return ColumnMismatchException(error_msg)


def reconcile_data(source: DataFrame, target: DataFrame, key_columns: list[str], report_type: str) -> ReconcileOutput:
    source_alias = "src"
    target_alias = "tgt"
    if report_type not in {"data", "all"}:
        key_columns = Constants.hash_column_name
    df = source.alias(source_alias).join(other=target.alias(target_alias), on=key_columns, how="full")

    mismatch = (
        _get_mismatch_data(df, source_alias, target_alias, source.columns) if report_type in {"all", "data"} else None
    )
    missing_in_src = (
        df.filter(col(f"{source_alias}.{Constants.hash_column_name}").isNull())
        .select((key_columns if report_type == "all" else alias_column_str(target_alias, target.columns)))
        .drop(Constants.hash_column_name)
    )
    missing_in_tgt = (
        df.filter(col(f"{target_alias}.{Constants.hash_column_name}").isNull())
        .select((key_columns if report_type == "all" else alias_column_str(source_alias, source.columns)))
        .drop(Constants.hash_column_name)
    )
    mismatch_count = 0
    if mismatch:
        mismatch_count = mismatch.count()

    return ReconcileOutput(
        mismatch_count=mismatch_count,
        missing_in_src_count=missing_in_src.count(),
        missing_in_tgt_count=missing_in_tgt.count(),
        missing_in_src=missing_in_src,
        missing_in_tgt=missing_in_tgt,
        mismatch=MismatchOutput(mismatch_df=mismatch),
    )


def _get_mismatch_data(df: DataFrame, src_alias: str, tgt_alias: str, select_columns) -> DataFrame:
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
        .select(alias_column_str(src_alias, select_columns))
        .drop(Constants.hash_column_name)
    )


def capture_mismatch_data_and_columns(source: DataFrame, target: DataFrame, key_columns: list[str]) -> MismatchOutput:
    source_columns = source.columns
    target_columns = target.columns

    if source_columns != target_columns:
        message = "source and target should have same columns for capturing the mismatch data"
        source_missing = [column for column in target_columns if column not in source_columns]
        target_missing = [column for column in source_columns if column not in target_columns]
        raise raise_column_mismatch_exception(message, source_missing, target_missing)

    check_columns = [column for column in source_columns if column not in key_columns]
    mismatch_df = _get_mismatch_df(source, target, key_columns, check_columns)
    mismatch_columns = _get_mismatch_columns(mismatch_df, check_columns)
    return MismatchOutput(mismatch_df, mismatch_columns)


def _get_mismatch_columns(df: DataFrame, columns: list[str]):
    mismatch_columns = []
    for column in columns:
        if df.where(~col(column + "_match")).take(1):
            mismatch_columns.append(column)
    return mismatch_columns


def _get_mismatch_df(source: DataFrame, target: DataFrame, key_columns: list[str], column_list: list[str]):
    source_aliased = [col('base.' + column).alias(column + '_base') for column in column_list]
    target_aliased = [col('compare.' + column).alias(column + '_compare') for column in column_list]

    match_expr = [expr(f"{column}_base=={column}_compare").alias(column + "_match") for column in column_list]
    select_expr = key_columns + source_aliased + target_aliased + match_expr

    filter_columns = " and ".join([column + "_match" for column in column_list])
    filter_expr = ~expr(filter_columns)

    mismatch_df = (
        source.alias('base')
        .join(other=target.alias('compare'), on=key_columns, how="inner")
        .select(select_expr)
        .filter(filter_expr)
    )
    compare_columns = [column for column in mismatch_df.columns if column not in key_columns]
    return mismatch_df.select(*key_columns + sorted(compare_columns))


def alias_column_str(alias: str, columns: list[str]) -> list[str]:
    return [f"{alias}.{column}" for column in columns]
