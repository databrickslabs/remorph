from dataclasses import dataclass

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, explode, udf, lit
from pyspark.sql.types import StringType


@dataclass
class TestReconReport:
    metrics: DataFrame
    missing_in_src: DataFrame
    missing_in_tgt: DataFrame
    mismatch: DataFrame
    threshold_mismatch: DataFrame


def _get_reconcile_report_data(spark, test_config):
    return spark.sql(
        f"""SELECT main.start_ts,recon_id,source_type,source_table,target_table,recon_type,status,recon_metrics,
        run_metrics,data as sample_data FROM (SELECT * FROM 
        {test_config.db_mock_catalog}.{test_config.db_mock_schema}.main WHERE main.start_ts = 
        (SELECT MAX(start_ts) FROM {test_config.db_mock_catalog}.{test_config.db_mock_schema}.main)) AS main 
        JOIN {test_config.db_mock_catalog}.{test_config.db_mock_schema}.metrics as metrics ON main.recon_table_id = 
        metrics.recon_table_id LEFT JOIN {test_config.db_mock_catalog}.{test_config.db_mock_schema}.details ON 
        main.recon_table_id = details.recon_table_id ORDER BY main.start_ts desc,
        main.recon_id,main.recon_table_id"""
    )


def _get_reconcile_metrics(report_data):
    return (
        report_data.select("recon_metrics")
        .distinct()
        .select(
            safe_struct_field("recon_metrics.row_comparison", lit("missing_in_source")).alias("missing_in_src"),
            safe_struct_field("recon_metrics.row_comparison", lit("missing_in_target")).alias("missing_in_tgt"),
            safe_struct_field("recon_metrics.column_comparison", lit("absolute_mismatch")).alias("mismatch"),
            safe_struct_field("recon_metrics.column_comparison", lit("threshold_mismatch")).alias("threshold_mismatch"),
            safe_struct_field("recon_metrics.column_comparison", lit("mismatch_columns")).alias("mismatch_columns"),
            safe_struct_field("recon_metrics", lit("schema_comparison")).alias("schema_valid"),
        )
    )


def _get_reconcile_details(report_data):
    return report_data.select(col("recon_type"), col("sample_data"))


def _get_reconcile_sample_data(recon_type, details, key_columns):
    return (
        details.where(col("recon_type") == recon_type)
        .select(explode(col("sample_data")).alias("sample_data_exploded"))
        .select(*[col(f"sample_data_exploded.{c}") for c in key_columns])
    )


def get_reports(spark, test_config, key_columns):
    validation_df = _get_reconcile_report_data(spark, test_config)
    metrics_df = _get_reconcile_metrics(validation_df)
    details_df = _get_reconcile_details(validation_df)
    missing_in_src = _get_reconcile_sample_data("missing_in_source", details_df, key_columns)
    missing_in_tgt = _get_reconcile_sample_data("missing_in_target", details_df, key_columns)
    mismatch = _get_reconcile_sample_data("mismatch", details_df, key_columns)
    threshold_mismatch = _get_reconcile_sample_data(
        "threshold_mismatch", details_df, [f"{c}_source" for c in key_columns]
    )

    return TestReconReport(
        metrics=metrics_df,
        missing_in_src=missing_in_src,
        missing_in_tgt=missing_in_tgt,
        mismatch=mismatch,
        threshold_mismatch=threshold_mismatch,
    )


def get_safe_struct_field(input_struct, field_name: str):
    if input_struct is not None and hasattr(input_struct, field_name):
        return getattr(input_struct, field_name)
    return None


safe_struct_field = udf(get_safe_struct_field, StringType())
