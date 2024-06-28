from dataclasses import dataclass

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, explode
from pyspark.sql.types import Row

from tests.integration.conftest import TestConfig


@dataclass
class TestReconReport:
    metrics: Row | None = None
    missing_in_src: DataFrame | None = None
    missing_in_tgt: DataFrame | None = None
    mismatch: DataFrame | None = None
    threshold_mismatch: DataFrame | None = None
    schema_validation: DataFrame | None = None


def _get_reconcile_report_data(spark: SparkSession, test_config: TestConfig) -> DataFrame:
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


def _get_reconcile_metrics(report_data: DataFrame) -> Row:
    return report_data.select("recon_metrics").distinct().collect()[0]


def _get_reconcile_details(report_data: DataFrame) -> DataFrame:
    return report_data.select(col("recon_type"), col("sample_data"))


def _get_reconcile_sample_data(recon_type: str, details: DataFrame, key_columns: list[str] | None) -> DataFrame:
    return (
        details.where(col("recon_type") == recon_type)
        .select(explode(col("sample_data")).alias("sample_data_exploded"))
        .select(*[col(f"sample_data_exploded.{c}") for c in key_columns])
    )


def get_reports(spark: SparkSession, test_config: TestConfig,
                report_type: str, key_columns: list[str] | None = None, ) -> TestReconReport:
    test_report = TestReconReport()
    validation_df = _get_reconcile_report_data(spark, test_config)
    test_report.metrics = _get_reconcile_metrics(validation_df)
    details_df = _get_reconcile_details(validation_df)
    if report_type in ("data", "all", "row"):
        test_report.missing_in_src = _get_reconcile_sample_data("missing_in_source", details_df, key_columns)
        test_report.missing_in_tgt = _get_reconcile_sample_data("missing_in_target", details_df, key_columns)
    if report_type in ("data", "all"):
        test_report.mismatch = _get_reconcile_sample_data("mismatch", details_df, key_columns)
        test_report.threshold_mismatch = _get_reconcile_sample_data(
            "threshold_mismatch", details_df, [f"{c}_source" for c in key_columns]
        )

    test_report.schema_validation = _get_reconcile_sample_data("schema", details_df,
                                                               ["source_column", "source_datatype",
                                                                "databricks_datatype", "is_valid"]).where(
        col("is_valid") == 'false')

    return test_report
