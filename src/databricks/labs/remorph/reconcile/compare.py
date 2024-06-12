import logging
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, expr, lit

from databricks.labs.remorph.reconcile.exception import ColumnMismatchException
from databricks.labs.remorph.reconcile.recon_capture import (
    ReconIntermediatePersist,
)
from databricks.labs.remorph.reconcile.recon_config import (
    DataReconcileOutput,
    MismatchOutput,
)

logger = logging.getLogger(__name__)

_HASH_COLUMN_NAME = "hash_value_recon"
_SAMPLE_ROWS = 50


def raise_column_mismatch_exception(msg: str, source_missing: list[str], target_missing: list[str]) -> Exception:
    error_msg = (
        f"{msg}\n"
        f"columns missing in source: {','.join(source_missing) if source_missing else None}\n"
        f"columns missing in target: {','.join(target_missing) if target_missing else None}\n"
    )
    return ColumnMismatchException(error_msg)


def reconcile_data(
    source: DataFrame,
    target: DataFrame,
    key_columns: list[str],
    report_type: str,
    spark: SparkSession,
    path: str,
) -> DataReconcileOutput:
    source_alias = "src"
    target_alias = "tgt"
    if report_type not in {"data", "all"}:
        key_columns = [_HASH_COLUMN_NAME]
    df = (
        source.alias(source_alias)
        .join(other=target.alias(target_alias), on=key_columns, how="full")
        .selectExpr(
            *[f'{source_alias}.{col_name} as {source_alias}_{col_name}' for col_name in source.columns],
            *[f'{target_alias}.{col_name} as {target_alias}_{col_name}' for col_name in target.columns],
        )
    )

    # Write unmatched df to volume
    df = ReconIntermediatePersist(spark, path).write_and_read_unmatched_df_with_volumes(df)
    logger.warning(f"Unmatched data is written to {path} successfully")

    mismatch = _get_mismatch_data(df, source_alias, target_alias) if report_type in {"all", "data"} else None

    missing_in_src = (
        df.filter(col(f"{source_alias}_{_HASH_COLUMN_NAME}").isNull())
        .select(
            *[
                col(col_name).alias(col_name.replace(f'{target_alias}_', '').lower())
                for col_name in df.columns
                if col_name.startswith(f'{target_alias}_')
            ]
        )
        .drop(_HASH_COLUMN_NAME)
    )

    missing_in_tgt = (
        df.filter(col(f"{target_alias}_{_HASH_COLUMN_NAME}").isNull())
        .select(
            *[
                col(col_name).alias(col_name.replace(f'{source_alias}_', '').lower())
                for col_name in df.columns
                if col_name.startswith(f'{source_alias}_')
            ]
        )
        .drop(_HASH_COLUMN_NAME)
    )
    mismatch_count = 0
    if mismatch:
        mismatch_count = mismatch.count()

    missing_in_src_count = missing_in_src.count()
    missing_in_tgt_count = missing_in_tgt.count()

    return DataReconcileOutput(
        mismatch_count=mismatch_count,
        missing_in_src_count=missing_in_src_count,
        missing_in_tgt_count=missing_in_tgt_count,
        missing_in_src=missing_in_src.limit(_SAMPLE_ROWS),
        missing_in_tgt=missing_in_tgt.limit(_SAMPLE_ROWS),
        mismatch=MismatchOutput(mismatch_df=mismatch),
    )


def _get_mismatch_data(df: DataFrame, src_alias: str, tgt_alias: str) -> DataFrame:
    return (
        df.filter(
            (col(f"{src_alias}_{_HASH_COLUMN_NAME}").isNotNull())
            & (col(f"{tgt_alias}_{_HASH_COLUMN_NAME}").isNotNull())
        )
        .withColumn(
            "hash_match",
            col(f"{src_alias}_{_HASH_COLUMN_NAME}") == col(f"{tgt_alias}_{_HASH_COLUMN_NAME}"),
        )
        .filter(col("hash_match") == lit(False))
        .select(
            *[
                col(col_name).alias(col_name.replace(f'{src_alias}_', '').lower())
                for col_name in df.columns
                if col_name.startswith(f'{src_alias}_')
            ]
        )
        .drop(_HASH_COLUMN_NAME)
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
    # Collect the DataFrame to a local variable
    local_df = df.collect()
    mismatch_columns = []
    for column in columns:
        # Check if any row has False in the column
        if any(not row[column + "_match"] for row in local_df):
            mismatch_columns.append(column)
    return mismatch_columns


def _get_mismatch_df(source: DataFrame, target: DataFrame, key_columns: list[str], column_list: list[str]):
    source_aliased = [col('base.' + column).alias(column + '_base') for column in column_list]
    target_aliased = [col('compare.' + column).alias(column + '_compare') for column in column_list]

    match_expr = [expr(f"{column}_base=={column}_compare").alias(column + "_match") for column in column_list]
    key_cols = [col(column) for column in key_columns]
    select_expr = key_cols + source_aliased + target_aliased + match_expr

    filter_columns = " and ".join([column + "_match" for column in column_list])
    filter_expr = ~expr(filter_columns)

    mismatch_df = (
        source.alias('base')
        .join(other=target.alias('compare'), on=key_columns, how="inner")
        .select(*select_expr)
        .filter(filter_expr)
    )
    compare_columns = [column for column in mismatch_df.columns if column not in key_columns]
    return mismatch_df.select(*key_columns + sorted(compare_columns))


def alias_column_str(alias: str, columns: list[str]) -> list[str]:
    return [f"{alias}.{column}" for column in columns]
