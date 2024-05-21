import datetime
import json
from unittest.mock import patch

import pytest
from pyspark.sql import Row, SparkSession
from pyspark.sql.functions import countDistinct
from pyspark.sql.types import BooleanType, StringType, StructField, StructType

from databricks.labs.remorph.config import DatabaseConfig, get_dialect
from databricks.labs.remorph.reconcile.exception import WriteToTableException
from databricks.labs.remorph.reconcile.recon_capture import ReconCapture
from databricks.labs.remorph.reconcile.recon_config import (
    MismatchOutput,
    ReconcileOutput,
    ReconcileProcessDuration,
    SchemaCompareOutput,
    Table,
    ThresholdOutput,
)


def data_prep(spark: SparkSession):
    # Mismatch DataFrame
    data = [
        Row(id=1, name_source='source1', name_target='target1', name_match='match1'),
        Row(id=2, name_source='source2', name_target='target2', name_match='match2'),
    ]
    mismatch_df = spark.createDataFrame(data)

    # Missing DataFrames
    data1 = [Row(id=1, name='name1'), Row(id=2, name='name2'), Row(id=3, name='name3')]
    data2 = [Row(id=1, name='name1'), Row(id=2, name='name2'), Row(id=3, name='name3'), Row(id=4, name='name4')]
    df1 = spark.createDataFrame(data1)
    df2 = spark.createDataFrame(data2)

    # Schema Compare Dataframe
    schema = StructType(
        [
            StructField("source_column", StringType(), True),
            StructField("source_datatype", StringType(), True),
            StructField("databricks_column", StringType(), True),
            StructField("databricks_datatype", StringType(), True),
            StructField("is_valid", BooleanType(), True),
        ]
    )
    data = [
        ("source_column1", "source_datatype1", "databricks_column1", "databricks_datatype1", True),
        ("source_column2", "source_datatype2", "databricks_column2", "databricks_datatype2", True),
        ("source_column3", "source_datatype3", "databricks_column3", "databricks_datatype3", True),
        ("source_column4", "source_datatype4", "databricks_column4", "databricks_datatype4", True),
    ]
    schema_df = spark.createDataFrame(data, schema)

    data = [
        Row(id=1, sal_source=1000, sal_target=1100, sal_match=True),
        Row(id=2, sal_source=2000, sal_target=2100, sal_match=False),
    ]
    threshold_df = spark.createDataFrame(data)

    # Prepare output dataclasses
    mismatch = MismatchOutput(mismatch_df=mismatch_df, mismatch_columns=["name"])
    threshold = ThresholdOutput(threshold_df, threshold_mismatch_count=2)
    reconcile_output = ReconcileOutput(
        mismatch_count=2,
        missing_in_src_count=3,
        missing_in_tgt_count=4,
        mismatch=mismatch,
        missing_in_src=df1,
        missing_in_tgt=df2,
        threshold_output=threshold,
    )
    schema_output = SchemaCompareOutput(is_valid=True, compare_df=schema_df)
    table_conf = Table(source_name="supplier", target_name="target_supplier")
    reconcile_process = ReconcileProcessDuration(
        start_ts=str(datetime.datetime.now()), end_ts=str(datetime.datetime.now())
    )

    # Drop old data
    spark.sql("DROP TABLE IF EXISTS DEFAULT.main")
    spark.sql("DROP TABLE IF EXISTS DEFAULT.metrics")
    spark.sql("DROP TABLE IF EXISTS DEFAULT.details")

    return reconcile_output, schema_output, table_conf, reconcile_process


def test_recon_capture_start(mock_workspace_client, mock_spark):
    database_config = DatabaseConfig(
        "source_test_schema", "target_test_catalog", "target_test_schema", "source_test_catalog"
    )
    ws = mock_workspace_client
    source_type = get_dialect("snowflake")
    spark = mock_spark
    recon_capture = ReconCapture(
        database_config,
        "73b44582-dbb7-489f-bad1-6a7e8f4821b1",
        "all",
        source_type,
        ws,
        spark,
    )
    reconcile_output, schema_output, table_conf, reconcile_process = data_prep(spark)
    with (
        patch(
            'databricks.labs.remorph.reconcile.recon_capture.ReconCapture._REMORPH_CATALOG_SCHEMA_NAME', new='default'
        ),
    ):
        recon_capture.start(
            reconcile_output=reconcile_output,
            schema_output=schema_output,
            table_conf=table_conf,
            recon_process_duration=reconcile_process,
        )

    # assert main
    remorph_recon_df = spark.sql("select * from DEFAULT.main")
    row = remorph_recon_df.collect()[0]
    assert remorph_recon_df.count() == 1
    assert row.recon_id == "73b44582-dbb7-489f-bad1-6a7e8f4821b1"
    assert row.source_table.col1 == "source_test_catalog"
    assert row.source_table.col2 == "source_test_schema"
    assert row.source_table.col3 == "supplier"
    assert row.target_table.col1 == "target_test_catalog"
    assert row.target_table.col2 == "target_test_schema"
    assert row.target_table.col3 == "target_supplier"
    assert row.report_type == "all"
    assert row.source_type == "Snowflake"

    # assert metrics
    remorph_recon_metrics_df = spark.sql("select * from DEFAULT.metrics")
    row = remorph_recon_metrics_df.collect()[0]
    assert remorph_recon_metrics_df.count() == 1
    assert row.recon_metrics.col1.col1 == 3
    assert row.recon_metrics.col1.col2 == 4
    assert row.recon_metrics.col2.col1 == 2
    assert row.recon_metrics.col2.col2 == 2
    assert row.recon_metrics.col2.col3 == "name"
    assert row.recon_metrics.col3 is True
    assert row.run_metrics.col1 is False
    assert row.run_metrics.col2 == "remorph"
    assert row.run_metrics.col3 == ""

    # assert details
    remorph_recon_details_df = spark.sql("select * from DEFAULT.details")
    assert remorph_recon_details_df.count() == 5
    assert remorph_recon_details_df.select("recon_type").distinct().count() == 5
    assert (
        remorph_recon_details_df.select("recon_table_id", "status")
        .groupby("recon_table_id")
        .agg(countDistinct("status").alias("count_stat"))
        .collect()[0]
        .count_stat
        == 2
    )
    assert json.dumps(remorph_recon_details_df.where("recon_type = 'mismatch'").select("data").collect()[0].data) == (
        "[{\"id\": \"1\", \"name_source\": \"source1\", \"name_target\": \"target1\", "
        "\"name_match\": \"match1\"}, {\"id\": \"2\", \"name_source\": \"source2\", "
        "\"name_target\": \"target2\", \"name_match\": \"match2\"}]"
    )

    rows = remorph_recon_details_df.orderBy("recon_type").collect()
    assert rows[0].recon_type == "mismatch"
    assert rows[0].status is False
    assert rows[1].recon_type == "missing_in_source"
    assert rows[1].status is False
    assert rows[2].recon_type == "missing_in_target"
    assert rows[2].status is False
    assert rows[3].recon_type == "schema"
    assert rows[3].status is True
    assert rows[4].recon_type == "threshold_mismatch"
    assert rows[4].status is False


def test_recon_capture_start_with_exception(mock_workspace_client, mock_spark):
    database_config = DatabaseConfig(
        "source_test_schema", "target_test_catalog", "target_test_schema", "source_test_catalog"
    )
    ws = mock_workspace_client
    source_type = get_dialect("snowflake")
    spark = mock_spark
    recon_capture = ReconCapture(
        database_config,
        "73b44582-dbb7-489f-bad1-6a7e8f4821b1",
        "all",
        source_type,
        ws,
        spark,
    )
    reconcile_output, schema_output, table_conf, reconcile_process = data_prep(spark)
    with (
        patch(
            'databricks.labs.remorph.reconcile.recon_capture.ReconCapture._REMORPH_CATALOG_SCHEMA_NAME', new='defaul'
        ),
    ) and pytest.raises(WriteToTableException):
        recon_capture.start(
            reconcile_output=reconcile_output,
            schema_output=schema_output,
            table_conf=table_conf,
            recon_process_duration=reconcile_process,
        )
