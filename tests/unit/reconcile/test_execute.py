from dataclasses import dataclass
from datetime import datetime
from unittest.mock import patch

import pytest
from pyspark import Row
from pyspark.errors import PySparkException
from pyspark.testing import assertDataFrameEqual

from databricks.labs.remorph.config import DatabaseConfig, TableRecon, get_dialect
from databricks.labs.remorph.reconcile.connectors.data_source import MockDataSource
from databricks.labs.remorph.reconcile.connectors.databricks import DatabricksDataSource
from databricks.labs.remorph.reconcile.connectors.snowflake import SnowflakeDataSource
from databricks.labs.remorph.reconcile.exception import DataSourceRuntimeException
from databricks.labs.remorph.reconcile.execute import (
    Reconciliation,
    initialise_data_source,
    recon,
)
from databricks.labs.remorph.reconcile.recon_config import (
    DataReconcileOutput,
    MismatchOutput,
    ThresholdOutput,
)
from databricks.labs.remorph.reconcile.schema_compare import SchemaCompare

CATALOG = "org"
SCHEMA = "data"
SRC_TABLE = "supplier"
TGT_TABLE = "target_supplier"


@dataclass
class QueryStore:
    source_hash_query: str
    target_hash_query: str
    source_mismatch_query: str
    target_mismatch_query: str
    source_missing_query: str
    target_missing_query: str
    source_threshold_query: str
    target_threshold_query: str
    threshold_comparison_query: str
    source_row_query: str
    target_row_query: str


@pytest.fixture
def setup_metadata_table(mock_spark, report_tables_schema):
    recon_schema, metrics_schema, details_schema = report_tables_schema
    mode = "append"
    mock_spark.createDataFrame(data=[], schema=recon_schema).write.mode(mode).saveAsTable("DEFAULT.MAIN")
    mock_spark.createDataFrame(data=[], schema=metrics_schema).write.mode(mode).saveAsTable("DEFAULT.METRICS")
    mock_spark.createDataFrame(data=[], schema=details_schema).write.mode(mode).saveAsTable("DEFAULT.DETAILS")
    yield
    mock_spark.sql("TRUNCATE TABLE DEFAULT.MAIN")
    mock_spark.sql("TRUNCATE TABLE DEFAULT.METRICS")
    mock_spark.sql("TRUNCATE TABLE DEFAULT.DETAILS")


@pytest.fixture
def query_store(mock_spark):
    source_hash_query = "SELECT LOWER(SHA2(CONCAT(TRIM(s_address), TRIM(s_name), COALESCE(TRIM(s_nationkey), ''), TRIM(s_phone), COALESCE(TRIM(s_suppkey), '')), 256)) AS hash_value_recon, s_nationkey AS s_nationkey, s_suppkey AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address = 'a'"
    target_hash_query = "SELECT LOWER(SHA2(CONCAT(TRIM(s_address_t), TRIM(s_name), COALESCE(TRIM(s_nationkey_t), ''), TRIM(s_phone_t), COALESCE(TRIM(s_suppkey_t), '')), 256)) AS hash_value_recon, s_nationkey_t AS s_nationkey, s_suppkey_t AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address_t = 'a'"
    source_mismatch_query = "WITH recon AS (SELECT 22 AS s_nationkey, 2 AS s_suppkey), src AS (SELECT TRIM(s_address) AS s_address, TRIM(s_name) AS s_name, COALESCE(TRIM(s_nationkey), '') AS s_nationkey, TRIM(s_phone) AS s_phone, COALESCE(TRIM(s_suppkey), '') AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address = 'a') SELECT s_address, s_name, s_nationkey, s_phone, s_suppkey FROM src INNER JOIN recon USING (s_nationkey, s_suppkey)"
    target_mismatch_query = "WITH recon AS (SELECT 22 AS s_nationkey, 2 AS s_suppkey), src AS (SELECT TRIM(s_address_t) AS s_address, TRIM(s_name) AS s_name, COALESCE(TRIM(s_nationkey_t), '') AS s_nationkey, TRIM(s_phone_t) AS s_phone, COALESCE(TRIM(s_suppkey_t), '') AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address_t = 'a') SELECT s_address, s_name, s_nationkey, s_phone, s_suppkey FROM src INNER JOIN recon USING (s_nationkey, s_suppkey)"
    source_missing_query = "WITH recon AS (SELECT 44 AS s_nationkey, 4 AS s_suppkey), src AS (SELECT TRIM(s_address_t) AS s_address, TRIM(s_name) AS s_name, COALESCE(TRIM(s_nationkey_t), '') AS s_nationkey, TRIM(s_phone_t) AS s_phone, COALESCE(TRIM(s_suppkey_t), '') AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address_t = 'a') SELECT s_address, s_name, s_nationkey, s_phone, s_suppkey FROM src INNER JOIN recon USING (s_nationkey, s_suppkey)"
    target_missing_query = "WITH recon AS (SELECT 33 AS s_nationkey, 3 AS s_suppkey), src AS (SELECT TRIM(s_address) AS s_address, TRIM(s_name) AS s_name, COALESCE(TRIM(s_nationkey), '') AS s_nationkey, TRIM(s_phone) AS s_phone, COALESCE(TRIM(s_suppkey), '') AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address = 'a') SELECT s_address, s_name, s_nationkey, s_phone, s_suppkey FROM src INNER JOIN recon USING (s_nationkey, s_suppkey)"
    source_threshold_query = "SELECT COALESCE(TRIM(s_nationkey), '') AS s_nationkey, COALESCE(TRIM(s_suppkey), '') AS s_suppkey, s_acctbal AS s_acctbal FROM :tbl WHERE s_name = 't' AND s_address = 'a'"
    target_threshold_query = "SELECT COALESCE(TRIM(s_nationkey_t), '') AS s_nationkey, COALESCE(TRIM(s_suppkey_t), '') AS s_suppkey, s_acctbal_t AS s_acctbal FROM :tbl WHERE s_name = 't' AND s_address_t = 'a'"
    threshold_comparison_query = "SELECT COALESCE(source.s_acctbal, 0) AS s_acctbal_source, COALESCE(databricks.s_acctbal, 0) AS s_acctbal_databricks, CASE WHEN (COALESCE(source.s_acctbal, 0) - COALESCE(databricks.s_acctbal, 0)) = 0 THEN 'Match' WHEN (COALESCE(source.s_acctbal, 0) - COALESCE(databricks.s_acctbal, 0)) BETWEEN 0 AND 100 THEN 'Warning' ELSE 'Failed' END AS s_acctbal_match, source.s_nationkey AS s_nationkey_source, source.s_suppkey AS s_suppkey_source FROM source_supplier_df_threshold_vw AS source INNER JOIN target_target_supplier_df_threshold_vw AS databricks ON source.s_nationkey <=> databricks.s_nationkey AND source.s_suppkey <=> databricks.s_suppkey WHERE (1 = 1 OR 1 = 1) OR (COALESCE(source.s_acctbal, 0) - COALESCE(databricks.s_acctbal, 0)) <> 0"
    source_row_query = "SELECT LOWER(SHA2(CONCAT(TRIM(s_address), TRIM(s_name), COALESCE(TRIM(s_nationkey), ''), TRIM(s_phone), COALESCE(TRIM(s_suppkey), '')), 256)) AS hash_value_recon, TRIM(s_address) AS s_address, TRIM(s_name) AS s_name, s_nationkey AS s_nationkey, TRIM(s_phone) AS s_phone, s_suppkey AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address = 'a'"
    target_row_query = "SELECT LOWER(SHA2(CONCAT(TRIM(s_address_t), TRIM(s_name), COALESCE(TRIM(s_nationkey_t), ''), TRIM(s_phone_t), COALESCE(TRIM(s_suppkey_t), '')), 256)) AS hash_value_recon, TRIM(s_address_t) AS s_address, TRIM(s_name) AS s_name, s_nationkey_t AS s_nationkey, TRIM(s_phone_t) AS s_phone, s_suppkey_t AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address_t = 'a'"

    return QueryStore(
        source_hash_query=source_hash_query,
        target_hash_query=target_hash_query,
        source_mismatch_query=source_mismatch_query,
        target_mismatch_query=target_mismatch_query,
        source_missing_query=source_missing_query,
        target_missing_query=target_missing_query,
        source_threshold_query=source_threshold_query,
        target_threshold_query=target_threshold_query,
        threshold_comparison_query=threshold_comparison_query,
        source_row_query=source_row_query,
        target_row_query=target_row_query,
    )


def test_reconcile_data_with_mismatches_and_missing(mock_spark, table_conf_with_opts, table_schema, query_store):
    src_schema, tgt_schema = table_schema

    source_dataframe_repository = {
        (
            CATALOG,
            SCHEMA,
            query_store.source_hash_query,
        ): mock_spark.createDataFrame(
            [
                Row(hash_value_recon="a1b", s_nationkey=11, s_suppkey=1),
                Row(hash_value_recon="c2d", s_nationkey=22, s_suppkey=2),
                Row(hash_value_recon="e3g", s_nationkey=33, s_suppkey=3),
            ]
        ),
        (CATALOG, SCHEMA, query_store.source_mismatch_query): mock_spark.createDataFrame(
            [Row(s_address="address-2", s_name="name-2", s_nationkey=22, s_phone="222-2", s_suppkey=2)]
        ),
        (CATALOG, SCHEMA, query_store.target_missing_query): mock_spark.createDataFrame(
            [Row(s_address="address-3", s_name="name-3", s_nationkey=33, s_phone="333", s_suppkey=3)]
        ),
        (CATALOG, SCHEMA, query_store.source_threshold_query): mock_spark.createDataFrame(
            [Row(s_nationkey=11, s_suppkey=1, s_acctbal=100)]
        ),
    }
    source_schema_repository = {(CATALOG, SCHEMA, SRC_TABLE): src_schema}

    target_dataframe_repository = {
        (
            CATALOG,
            SCHEMA,
            query_store.target_hash_query,
        ): mock_spark.createDataFrame(
            [
                Row(hash_value_recon="a1b", s_nationkey=11, s_suppkey=1),
                Row(hash_value_recon="c2de", s_nationkey=22, s_suppkey=2),
                Row(hash_value_recon="k4l", s_nationkey=44, s_suppkey=4),
            ]
        ),
        (CATALOG, SCHEMA, query_store.target_mismatch_query): mock_spark.createDataFrame(
            [Row(s_address="address-22", s_name="name-2", s_nationkey=22, s_phone="222", s_suppkey=2)]
        ),
        (CATALOG, SCHEMA, query_store.source_missing_query): mock_spark.createDataFrame(
            [Row(s_address="address-4", s_name="name-4", s_nationkey=44, s_phone="444", s_suppkey=4)]
        ),
        (CATALOG, SCHEMA, query_store.target_threshold_query): mock_spark.createDataFrame(
            [Row(s_nationkey=11, s_suppkey=1, s_acctbal=210)]
        ),
        (CATALOG, SCHEMA, query_store.threshold_comparison_query): mock_spark.createDataFrame(
            [
                Row(
                    s_acctbal_source=100,
                    s_acctbal_databricks=210,
                    s_acctbal_match="Failed",
                    s_nationkey_source=11,
                    s_suppkey_source=1,
                )
            ]
        ),
    }

    target_schema_repository = {(CATALOG, SCHEMA, TGT_TABLE): tgt_schema}
    database_config = DatabaseConfig(
        source_catalog=CATALOG,
        source_schema=SCHEMA,
        target_catalog=CATALOG,
        target_schema=SCHEMA,
    )
    schema_comparator = SchemaCompare(mock_spark)
    source = MockDataSource(source_dataframe_repository, source_schema_repository)
    target = MockDataSource(target_dataframe_repository, target_schema_repository)
    reconciler = Reconciliation(source, target, database_config, "data", schema_comparator, get_dialect("databricks"))
    actual_data_reconcile = reconciler.reconcile_data(table_conf_with_opts, src_schema, tgt_schema)
    expected_data_reconcile = DataReconcileOutput(
        mismatch_count=1,
        missing_in_src_count=1,
        missing_in_tgt_count=1,
        missing_in_src=mock_spark.createDataFrame(
            [Row(s_address="address-4", s_name="name-4", s_nationkey=44, s_phone="444", s_suppkey=4)]
        ),
        missing_in_tgt=mock_spark.createDataFrame(
            [Row(s_address="address-3", s_name="name-3", s_nationkey=33, s_phone="333", s_suppkey=3)]
        ),
        mismatch=MismatchOutput(
            mismatch_df=mock_spark.createDataFrame(
                [
                    Row(
                        s_suppkey=2,
                        s_nationkey=22,
                        s_address_base="address-2",
                        s_address_compare="address-22",
                        s_address_match=False,
                        s_name_base="name-2",
                        s_name_compare="name-2",
                        s_name_match=True,
                        s_phone_base="222-2",
                        s_phone_compare="222",
                        s_phone_match=False,
                    )
                ]
            ),
            mismatch_columns=["s_address", "s_phone"],
        ),
        threshold_output=ThresholdOutput(
            threshold_df=mock_spark.createDataFrame(
                [
                    Row(
                        s_acctbal_source=100,
                        s_acctbal_databricks=210,
                        s_acctbal_match="Failed",
                        s_nationkey_source=11,
                        s_suppkey_source=1,
                    )
                ]
            ),
            threshold_mismatch_count=1,
        ),
    )

    assert actual_data_reconcile.mismatch_count == expected_data_reconcile.mismatch_count
    assert actual_data_reconcile.missing_in_src_count == expected_data_reconcile.missing_in_src_count
    assert actual_data_reconcile.missing_in_tgt_count == expected_data_reconcile.missing_in_tgt_count
    assert actual_data_reconcile.mismatch.mismatch_columns == expected_data_reconcile.mismatch.mismatch_columns

    assertDataFrameEqual(actual_data_reconcile.mismatch.mismatch_df, expected_data_reconcile.mismatch.mismatch_df)
    assertDataFrameEqual(actual_data_reconcile.missing_in_src, expected_data_reconcile.missing_in_src)
    assertDataFrameEqual(actual_data_reconcile.missing_in_tgt, expected_data_reconcile.missing_in_tgt)

    actual_schema_reconcile = reconciler.reconcile_schema(src_schema, tgt_schema, table_conf_with_opts)
    expected_schema_reconcile = mock_spark.createDataFrame(
        [
            Row(
                source_column="s_suppkey",
                source_datatype="number",
                databricks_column="s_suppkey_t",
                databricks_datatype="number",
                is_valid=True,
            ),
            Row(
                source_column="s_name",
                source_datatype="varchar",
                databricks_column="s_name",
                databricks_datatype="varchar",
                is_valid=True,
            ),
            Row(
                source_column="s_address",
                source_datatype="varchar",
                databricks_column="s_address_t",
                databricks_datatype="varchar",
                is_valid=True,
            ),
            Row(
                source_column="s_nationkey",
                source_datatype="number",
                databricks_column="s_nationkey_t",
                databricks_datatype="number",
                is_valid=True,
            ),
            Row(
                source_column="s_phone",
                source_datatype="varchar",
                databricks_column="s_phone_t",
                databricks_datatype="varchar",
                is_valid=True,
            ),
            Row(
                source_column="s_acctbal",
                source_datatype="number",
                databricks_column="s_acctbal_t",
                databricks_datatype="number",
                is_valid=True,
            ),
        ]
    )
    assertDataFrameEqual(actual_schema_reconcile.compare_df, expected_schema_reconcile)
    assert actual_schema_reconcile.is_valid is True

    assertDataFrameEqual(
        actual_data_reconcile.threshold_output.threshold_df,
        mock_spark.createDataFrame(
            [
                Row(
                    s_acctbal_source=100,
                    s_acctbal_databricks=210,
                    s_acctbal_match="Failed",
                    s_nationkey_source=11,
                    s_suppkey_source=1,
                )
            ]
        ),
    )
    assert actual_data_reconcile.threshold_output.threshold_mismatch_count == 1


def test_reconcile_data_without_mismatches_and_missing(
    mock_spark,
    table_conf_with_opts,
    table_schema,
    query_store,
):
    src_schema, tgt_schema = table_schema
    source_dataframe_repository = {
        (
            CATALOG,
            SCHEMA,
            query_store.source_hash_query,
        ): mock_spark.createDataFrame(
            [
                Row(hash_value_recon="a1b", s_nationkey=11, s_suppkey=1),
                Row(hash_value_recon="c2d", s_nationkey=22, s_suppkey=2),
            ]
        ),
        (CATALOG, SCHEMA, query_store.source_threshold_query): mock_spark.createDataFrame(
            [Row(s_nationkey=11, s_suppkey=1, s_acctbal=100)]
        ),
    }
    source_schema_repository = {(CATALOG, SCHEMA, SRC_TABLE): src_schema}

    target_dataframe_repository = {
        (
            CATALOG,
            SCHEMA,
            query_store.target_hash_query,
        ): mock_spark.createDataFrame(
            [
                Row(hash_value_recon="a1b", s_nationkey=11, s_suppkey=1),
                Row(hash_value_recon="c2d", s_nationkey=22, s_suppkey=2),
            ]
        ),
        (CATALOG, SCHEMA, query_store.target_threshold_query): mock_spark.createDataFrame(
            [Row(s_nationkey=11, s_suppkey=1, s_acctbal=110)]
        ),
        (CATALOG, SCHEMA, query_store.threshold_comparison_query): mock_spark.createDataFrame(
            [
                Row(
                    s_acctbal_source=100,
                    s_acctbal_databricks=110,
                    s_acctbal_match="Warning",
                    s_nationkey_source=11,
                    s_suppkey_source=1,
                )
            ]
        ),
    }

    target_schema_repository = {(CATALOG, SCHEMA, TGT_TABLE): tgt_schema}
    database_config = DatabaseConfig(
        source_catalog=CATALOG,
        source_schema=SCHEMA,
        target_catalog=CATALOG,
        target_schema=SCHEMA,
    )
    schema_comparator = SchemaCompare(mock_spark)
    source = MockDataSource(source_dataframe_repository, source_schema_repository)
    target = MockDataSource(target_dataframe_repository, target_schema_repository)
    actual = Reconciliation(
        source, target, database_config, "data", schema_comparator, get_dialect("databricks")
    ).reconcile_data(table_conf_with_opts, src_schema, tgt_schema)

    assert actual.mismatch_count == 0
    assert actual.missing_in_src_count == 0
    assert actual.missing_in_tgt_count == 0
    assert actual.mismatch is None
    assert actual.missing_in_src is None
    assert actual.missing_in_tgt is None
    assert actual.threshold_output.threshold_df is None
    assert actual.threshold_output.threshold_mismatch_count == 0


def test_reconcile_data_with_mismatch_and_no_missing(mock_spark, table_conf_with_opts, table_schema, query_store):
    src_schema, tgt_schema = table_schema
    table_conf_with_opts.drop_columns = ["s_acctbal"]
    table_conf_with_opts.thresholds = None
    source_dataframe_repository = {
        (
            CATALOG,
            SCHEMA,
            query_store.source_hash_query,
        ): mock_spark.createDataFrame(
            [
                Row(hash_value_recon="a1b", s_nationkey=11, s_suppkey=1),
                Row(hash_value_recon="c2d", s_nationkey=22, s_suppkey=2),
            ]
        ),
        (CATALOG, SCHEMA, query_store.source_mismatch_query): mock_spark.createDataFrame(
            [Row(s_address="address-2", s_name="name-2", s_nationkey=22, s_phone="222-2", s_suppkey=2)]
        ),
    }
    source_schema_repository = {(CATALOG, SCHEMA, SRC_TABLE): src_schema}

    target_dataframe_repository = {
        (
            CATALOG,
            SCHEMA,
            query_store.target_hash_query,
        ): mock_spark.createDataFrame(
            [
                Row(hash_value_recon="a1b", s_nationkey=11, s_suppkey=1),
                Row(hash_value_recon="c2de", s_nationkey=22, s_suppkey=2),
            ]
        ),
        (CATALOG, SCHEMA, query_store.target_mismatch_query): mock_spark.createDataFrame(
            [Row(s_address="address-22", s_name="name-2", s_nationkey=22, s_phone="222", s_suppkey=2)]
        ),
    }

    target_schema_repository = {(CATALOG, SCHEMA, TGT_TABLE): tgt_schema}
    database_config = DatabaseConfig(
        source_catalog=CATALOG,
        source_schema=SCHEMA,
        target_catalog=CATALOG,
        target_schema=SCHEMA,
    )
    schema_comparator = SchemaCompare(mock_spark)
    source = MockDataSource(source_dataframe_repository, source_schema_repository)
    target = MockDataSource(target_dataframe_repository, target_schema_repository)
    actual = Reconciliation(
        source, target, database_config, "data", schema_comparator, get_dialect("databricks")
    ).reconcile_data(table_conf_with_opts, src_schema, tgt_schema)
    expected = DataReconcileOutput(
        mismatch_count=1,
        missing_in_src_count=0,
        missing_in_tgt_count=0,
        missing_in_src=None,
        missing_in_tgt=None,
        mismatch=MismatchOutput(
            mismatch_df=mock_spark.createDataFrame(
                [
                    Row(
                        s_suppkey=2,
                        s_nationkey=22,
                        s_address_base="address-2",
                        s_address_compare="address-22",
                        s_address_match=False,
                        s_name_base="name-2",
                        s_name_compare="name-2",
                        s_name_match=True,
                        s_phone_base="222-2",
                        s_phone_compare="222",
                        s_phone_match=False,
                    )
                ]
            ),
            mismatch_columns=["s_address", "s_phone"],
        ),
    )

    assert actual.mismatch_count == expected.mismatch_count
    assert actual.missing_in_src_count == expected.missing_in_src_count
    assert actual.missing_in_tgt_count == expected.missing_in_tgt_count
    assert actual.mismatch.mismatch_columns == expected.mismatch.mismatch_columns
    assert actual.missing_in_src is None
    assert actual.missing_in_tgt is None

    assertDataFrameEqual(actual.mismatch.mismatch_df, expected.mismatch.mismatch_df)


def test_reconcile_data_missing_and_no_mismatch(mock_spark, table_conf_with_opts, table_schema, query_store):
    src_schema, tgt_schema = table_schema
    table_conf_with_opts.drop_columns = ["s_acctbal"]
    table_conf_with_opts.thresholds = None
    source_dataframe_repository = {
        (
            CATALOG,
            SCHEMA,
            query_store.source_hash_query,
        ): mock_spark.createDataFrame(
            [
                Row(hash_value_recon="a1b", s_nationkey=11, s_suppkey=1),
                Row(hash_value_recon="c2d", s_nationkey=22, s_suppkey=2),
                Row(hash_value_recon="e3g", s_nationkey=33, s_suppkey=3),
            ]
        ),
        (CATALOG, SCHEMA, query_store.target_missing_query): mock_spark.createDataFrame(
            [Row(s_address="address-3", s_name="name-3", s_nationkey=33, s_phone="333", s_suppkey=3)]
        ),
    }
    source_schema_repository = {(CATALOG, SCHEMA, SRC_TABLE): src_schema}

    target_dataframe_repository = {
        (
            CATALOG,
            SCHEMA,
            query_store.target_hash_query,
        ): mock_spark.createDataFrame(
            [
                Row(hash_value_recon="a1b", s_nationkey=11, s_suppkey=1),
                Row(hash_value_recon="c2d", s_nationkey=22, s_suppkey=2),
                Row(hash_value_recon="k4l", s_nationkey=44, s_suppkey=4),
            ]
        ),
        (CATALOG, SCHEMA, query_store.source_missing_query): mock_spark.createDataFrame(
            [Row(s_address="address-4", s_name="name-4", s_nationkey=44, s_phone="444", s_suppkey=4)]
        ),
    }

    target_schema_repository = {(CATALOG, SCHEMA, TGT_TABLE): tgt_schema}
    database_config = DatabaseConfig(
        source_catalog=CATALOG,
        source_schema=SCHEMA,
        target_catalog=CATALOG,
        target_schema=SCHEMA,
    )
    schema_comparator = SchemaCompare(mock_spark)
    source = MockDataSource(source_dataframe_repository, source_schema_repository)
    target = MockDataSource(target_dataframe_repository, target_schema_repository)
    actual = Reconciliation(
        source, target, database_config, "data", schema_comparator, get_dialect("databricks")
    ).reconcile_data(table_conf_with_opts, src_schema, tgt_schema)
    expected = DataReconcileOutput(
        mismatch_count=0,
        missing_in_src_count=1,
        missing_in_tgt_count=1,
        missing_in_src=mock_spark.createDataFrame(
            [Row(s_address="address-4", s_name="name-4", s_nationkey=44, s_phone="444", s_suppkey=4)]
        ),
        missing_in_tgt=mock_spark.createDataFrame(
            [Row(s_address="address-3", s_name="name-3", s_nationkey=33, s_phone="333", s_suppkey=3)]
        ),
        mismatch=None,
    )

    assert actual.mismatch_count == expected.mismatch_count
    assert actual.missing_in_src_count == expected.missing_in_src_count
    assert actual.missing_in_tgt_count == expected.missing_in_tgt_count
    assert actual.mismatch is None

    assertDataFrameEqual(actual.missing_in_src, expected.missing_in_src)
    assertDataFrameEqual(actual.missing_in_tgt, expected.missing_in_tgt)


@pytest.fixture
def mock_for_report_type_data(
    table_conf_with_opts,
    table_schema,
    query_store,
    setup_metadata_table,
    mock_spark,
):
    table_conf_with_opts.drop_columns = ["s_acctbal"]
    table_conf_with_opts.thresholds = None
    table_recon = TableRecon(
        source_catalog="org",
        source_schema="data",
        target_catalog="org",
        target_schema="data",
        tables=[table_conf_with_opts],
    )
    src_schema, tgt_schema = table_schema
    source_dataframe_repository = {
        (
            CATALOG,
            SCHEMA,
            query_store.source_hash_query,
        ): mock_spark.createDataFrame(
            [
                Row(hash_value_recon="a1b", s_nationkey=11, s_suppkey=1),
                Row(hash_value_recon="c2d", s_nationkey=22, s_suppkey=2),
                Row(hash_value_recon="e3g", s_nationkey=33, s_suppkey=3),
            ]
        ),
        (CATALOG, SCHEMA, query_store.source_mismatch_query): mock_spark.createDataFrame(
            [Row(s_address="address-2", s_name="name-2", s_nationkey=22, s_phone="222-2", s_suppkey=2)]
        ),
        (CATALOG, SCHEMA, query_store.target_missing_query): mock_spark.createDataFrame(
            [Row(s_address="address-3", s_name="name-3", s_nationkey=33, s_phone="333", s_suppkey=3)]
        ),
    }
    source_schema_repository = {(CATALOG, SCHEMA, SRC_TABLE): src_schema}

    target_dataframe_repository = {
        (
            CATALOG,
            SCHEMA,
            query_store.target_hash_query,
        ): mock_spark.createDataFrame(
            [
                Row(hash_value_recon="a1b", s_nationkey=11, s_suppkey=1),
                Row(hash_value_recon="c2de", s_nationkey=22, s_suppkey=2),
                Row(hash_value_recon="k4l", s_nationkey=44, s_suppkey=4),
            ]
        ),
        (CATALOG, SCHEMA, query_store.target_mismatch_query): mock_spark.createDataFrame(
            [Row(s_address="address-22", s_name="name-2", s_nationkey=22, s_phone="222", s_suppkey=2)]
        ),
        (CATALOG, SCHEMA, query_store.source_missing_query): mock_spark.createDataFrame(
            [Row(s_address="address-4", s_name="name-4", s_nationkey=44, s_phone="444", s_suppkey=4)]
        ),
    }

    target_schema_repository = {(CATALOG, SCHEMA, TGT_TABLE): tgt_schema}
    source = MockDataSource(source_dataframe_repository, source_schema_repository)
    target = MockDataSource(target_dataframe_repository, target_schema_repository)

    return table_recon, source, target


def test_recon_for_report_type_is_data(
    mock_workspace_client, mock_spark, report_tables_schema, mock_for_report_type_data
):
    recon_schema, metrics_schema, details_schema = report_tables_schema
    table_recon, source, target = mock_for_report_type_data
    with (
        patch("databricks.labs.remorph.reconcile.execute.datetime") as mock_datetime,
        patch("databricks.labs.remorph.reconcile.recon_capture.datetime") as recon_datetime,
        patch("databricks.labs.remorph.reconcile.execute.initialise_data_source", return_value=(source, target)),
        patch("databricks.labs.remorph.reconcile.execute.uuid4", return_value="00112233-4455-6677-8899-aabbccddeeff"),
        patch("databricks.labs.remorph.reconcile.recon_capture.ReconCapture._DB_PREFIX", new="default"),
        patch(
            "databricks.labs.remorph.reconcile.recon_capture.ReconCapture._generate_recon_main_id", return_value=11111
        ),
    ):
        mock_datetime.now.return_value = datetime(2024, 5, 23, 9, 21, 25, 122185)
        recon_datetime.now.return_value = datetime(2024, 5, 23, 9, 21, 25, 122185)
        recon_id = recon(mock_workspace_client, mock_spark, table_recon, get_dialect("databricks"), "data")

    actual_remorph_recon = mock_spark.sql("SELECT * FROM DEFAULT.MAIN")
    actual_remorph_recon_metrics = mock_spark.sql("SELECT * FROM DEFAULT.METRICS")
    actual_remorph_recon_details = mock_spark.sql("SELECT * FROM DEFAULT.DETAILS")

    expected_remorph_recon = mock_spark.createDataFrame(
        data=[
            (
                11111,
                "00112233-4455-6677-8899-aabbccddeeff",
                "Databricks",
                ("org", "data", "supplier"),
                ("org", "data", "target_supplier"),
                "data",
                datetime(2024, 5, 23, 9, 21, 25, 122185),
                datetime(2024, 5, 23, 9, 21, 25, 122185),
            )
        ],
        schema=recon_schema,
    )
    expected_remorph_recon_metrics = mock_spark.createDataFrame(
        data=[
            (
                11111,
                ((1, 1), (1, 0, "s_address,s_phone"), True),
                (False, "remorph", ""),
                datetime(2024, 5, 23, 9, 21, 25, 122185),
            )
        ],
        schema=metrics_schema,
    )
    expected_remorph_recon_details = mock_spark.createDataFrame(
        data=[
            (
                11111,
                "mismatch",
                False,
                [
                    {
                        "s_suppkey": "2",
                        "s_nationkey": "22",
                        "s_address_base": "address-2",
                        "s_address_compare": "address-22",
                        "s_address_match": "false",
                        "s_name_base": "name-2",
                        "s_name_compare": "name-2",
                        "s_name_match": "true",
                        "s_phone_base": "222-2",
                        "s_phone_compare": "222",
                        "s_phone_match": "false",
                    }
                ],
                datetime(2024, 5, 23, 9, 21, 25, 122185),
            ),
            (
                11111,
                "missing_in_source",
                False,
                [
                    {
                        "s_address": "address-4",
                        "s_name": "name-4",
                        "s_nationkey": "44",
                        "s_phone": "444",
                        "s_suppkey": "4",
                    }
                ],
                datetime(2024, 5, 23, 9, 21, 25, 122185),
            ),
            (
                11111,
                "missing_in_target",
                False,
                [
                    {
                        "s_address": "address-3",
                        "s_name": "name-3",
                        "s_nationkey": "33",
                        "s_phone": "333",
                        "s_suppkey": "3",
                    }
                ],
                datetime(2024, 5, 23, 9, 21, 25, 122185),
            ),
        ],
        schema=details_schema,
    )

    assertDataFrameEqual(actual_remorph_recon, expected_remorph_recon, ignoreNullable=True)
    assertDataFrameEqual(actual_remorph_recon_metrics, expected_remorph_recon_metrics, ignoreNullable=True)
    assertDataFrameEqual(actual_remorph_recon_details, expected_remorph_recon_details, ignoreNullable=True)

    assert recon_id == "00112233-4455-6677-8899-aabbccddeeff"


@pytest.fixture
def mock_for_report_type_schema(table_conf_with_opts, table_schema, query_store, mock_spark, setup_metadata_table):
    table_recon = TableRecon(
        source_catalog="org",
        source_schema="data",
        target_catalog="org",
        target_schema="data",
        tables=[table_conf_with_opts],
    )
    src_schema, tgt_schema = table_schema
    source_dataframe_repository = {
        (
            CATALOG,
            SCHEMA,
            query_store.source_hash_query,
        ): mock_spark.createDataFrame(
            [
                Row(hash_value_recon="a1b", s_nationkey=11, s_suppkey=1),
                Row(hash_value_recon="c2d", s_nationkey=22, s_suppkey=2),
                Row(hash_value_recon="e3g", s_nationkey=33, s_suppkey=3),
            ]
        ),
        (CATALOG, SCHEMA, query_store.source_mismatch_query): mock_spark.createDataFrame(
            [Row(s_address="address-2", s_name="name-2", s_nationkey=22, s_phone="222-2", s_suppkey=2)]
        ),
        (CATALOG, SCHEMA, query_store.target_missing_query): mock_spark.createDataFrame(
            [Row(s_address="address-3", s_name="name-3", s_nationkey=33, s_phone="333", s_suppkey=3)]
        ),
    }
    source_schema_repository = {(CATALOG, SCHEMA, SRC_TABLE): src_schema}

    target_dataframe_repository = {
        (
            CATALOG,
            SCHEMA,
            query_store.target_hash_query,
        ): mock_spark.createDataFrame(
            [
                Row(hash_value_recon="a1b", s_nationkey=11, s_suppkey=1),
                Row(hash_value_recon="c2de", s_nationkey=22, s_suppkey=2),
                Row(hash_value_recon="k4l", s_nationkey=44, s_suppkey=4),
            ]
        ),
        (CATALOG, SCHEMA, query_store.target_mismatch_query): mock_spark.createDataFrame(
            [Row(s_address="address-22", s_name="name-2", s_nationkey=22, s_phone="222", s_suppkey=2)]
        ),
        (CATALOG, SCHEMA, query_store.source_missing_query): mock_spark.createDataFrame(
            [Row(s_address="address-4", s_name="name-4", s_nationkey=44, s_phone="444", s_suppkey=4)]
        ),
    }

    target_schema_repository = {(CATALOG, SCHEMA, TGT_TABLE): tgt_schema}
    source = MockDataSource(source_dataframe_repository, source_schema_repository)
    target = MockDataSource(target_dataframe_repository, target_schema_repository)

    return table_recon, source, target


def test_recon_for_report_type_schema(
    mock_workspace_client, mock_spark, report_tables_schema, mock_for_report_type_schema
):
    recon_schema, metrics_schema, details_schema = report_tables_schema
    table_recon, source, target = mock_for_report_type_schema
    with (
        patch("databricks.labs.remorph.reconcile.execute.datetime") as mock_datetime,
        patch("databricks.labs.remorph.reconcile.recon_capture.datetime") as recon_datetime,
        patch("databricks.labs.remorph.reconcile.execute.initialise_data_source", return_value=(source, target)),
        patch("databricks.labs.remorph.reconcile.execute.uuid4", return_value="00112233-4455-6677-8899-aabbccddeeff"),
        patch("databricks.labs.remorph.reconcile.recon_capture.ReconCapture._DB_PREFIX", new="default"),
        patch(
            "databricks.labs.remorph.reconcile.recon_capture.ReconCapture._generate_recon_main_id", return_value=22222
        ),
    ):
        mock_datetime.now.return_value = datetime(2024, 5, 23, 9, 21, 25, 122185)
        recon_datetime.now.return_value = datetime(2024, 5, 23, 9, 21, 25, 122185)
        recon_id = recon(mock_workspace_client, mock_spark, table_recon, get_dialect("databricks"), "schema")

    actual_remorph_recon = mock_spark.sql("SELECT * FROM DEFAULT.MAIN")
    actual_remorph_recon_metrics = mock_spark.sql("SELECT * FROM DEFAULT.METRICS")
    actual_remorph_recon_details = mock_spark.sql("SELECT * FROM DEFAULT.DETAILS")

    expected_remorph_recon = mock_spark.createDataFrame(
        data=[
            (
                22222,
                "00112233-4455-6677-8899-aabbccddeeff",
                "Databricks",
                ("org", "data", "supplier"),
                ("org", "data", "target_supplier"),
                "schema",
                datetime(2024, 5, 23, 9, 21, 25, 122185),
                datetime(2024, 5, 23, 9, 21, 25, 122185),
            )
        ],
        schema=recon_schema,
    )
    expected_remorph_recon_metrics = mock_spark.createDataFrame(
        data=[(22222, ((0, 0), (0, 0, ""), True), (True, "remorph", ""), datetime(2024, 5, 23, 9, 21, 25, 122185))],
        schema=metrics_schema,
    )
    expected_remorph_recon_details = mock_spark.createDataFrame(
        data=[
            (
                22222,
                "schema",
                True,
                [
                    {
                        "source_column": "s_suppkey",
                        "source_datatype": "number",
                        "databricks_column": "s_suppkey_t",
                        "databricks_datatype": "number",
                        "is_valid": "true",
                    },
                    {
                        "source_column": "s_name",
                        "source_datatype": "varchar",
                        "databricks_column": "s_name",
                        "databricks_datatype": "varchar",
                        "is_valid": "true",
                    },
                    {
                        "source_column": "s_address",
                        "source_datatype": "varchar",
                        "databricks_column": "s_address_t",
                        "databricks_datatype": "varchar",
                        "is_valid": "true",
                    },
                    {
                        "source_column": "s_nationkey",
                        "source_datatype": "number",
                        "databricks_column": "s_nationkey_t",
                        "databricks_datatype": "number",
                        "is_valid": "true",
                    },
                    {
                        "source_column": "s_phone",
                        "source_datatype": "varchar",
                        "databricks_column": "s_phone_t",
                        "databricks_datatype": "varchar",
                        "is_valid": "true",
                    },
                    {
                        "source_column": "s_acctbal",
                        "source_datatype": "number",
                        "databricks_column": "s_acctbal_t",
                        "databricks_datatype": "number",
                        "is_valid": "true",
                    },
                ],
                datetime(2024, 5, 23, 9, 21, 25, 122185),
            )
        ],
        schema=details_schema,
    )

    assertDataFrameEqual(actual_remorph_recon, expected_remorph_recon, ignoreNullable=True)
    assertDataFrameEqual(actual_remorph_recon_metrics, expected_remorph_recon_metrics, ignoreNullable=True)
    assertDataFrameEqual(actual_remorph_recon_details, expected_remorph_recon_details, ignoreNullable=True)

    assert recon_id == "00112233-4455-6677-8899-aabbccddeeff"


@pytest.fixture
def mock_for_report_type_all(
    mock_workspace_client,
    table_conf_with_opts,
    table_schema,
    mock_spark,
    query_store,
    setup_metadata_table,
):
    table_conf_with_opts.drop_columns = ["s_acctbal"]
    table_conf_with_opts.thresholds = None
    table_recon = TableRecon(
        source_catalog="org",
        source_schema="data",
        target_catalog="org",
        target_schema="data",
        tables=[table_conf_with_opts],
    )
    src_schema, tgt_schema = table_schema
    source_dataframe_repository = {
        (
            CATALOG,
            SCHEMA,
            query_store.source_hash_query,
        ): mock_spark.createDataFrame(
            [
                Row(hash_value_recon="a1b", s_nationkey=11, s_suppkey=1),
                Row(hash_value_recon="c2d", s_nationkey=22, s_suppkey=2),
                Row(hash_value_recon="e3g", s_nationkey=33, s_suppkey=3),
            ]
        ),
        (CATALOG, SCHEMA, query_store.source_mismatch_query): mock_spark.createDataFrame(
            [Row(s_address="address-2", s_name="name-2", s_nationkey=22, s_phone="222-2", s_suppkey=2)]
        ),
        (CATALOG, SCHEMA, query_store.target_missing_query): mock_spark.createDataFrame(
            [Row(s_address="address-3", s_name="name-3", s_nationkey=33, s_phone="333", s_suppkey=3)]
        ),
    }
    source_schema_repository = {(CATALOG, SCHEMA, SRC_TABLE): src_schema}

    target_dataframe_repository = {
        (
            CATALOG,
            SCHEMA,
            query_store.target_hash_query,
        ): mock_spark.createDataFrame(
            [
                Row(hash_value_recon="a1b", s_nationkey=11, s_suppkey=1),
                Row(hash_value_recon="c2de", s_nationkey=22, s_suppkey=2),
                Row(hash_value_recon="k4l", s_nationkey=44, s_suppkey=4),
            ]
        ),
        (CATALOG, SCHEMA, query_store.target_mismatch_query): mock_spark.createDataFrame(
            [Row(s_address="address-22", s_name="name-2", s_nationkey=22, s_phone="222", s_suppkey=2)]
        ),
        (CATALOG, SCHEMA, query_store.source_missing_query): mock_spark.createDataFrame(
            [Row(s_address="address-4", s_name="name-4", s_nationkey=44, s_phone="444", s_suppkey=4)]
        ),
    }

    target_schema_repository = {(CATALOG, SCHEMA, TGT_TABLE): tgt_schema}
    source = MockDataSource(source_dataframe_repository, source_schema_repository)
    target = MockDataSource(target_dataframe_repository, target_schema_repository)
    return table_recon, source, target


def test_recon_for_report_type_all(mock_workspace_client, mock_spark, report_tables_schema, mock_for_report_type_all):
    recon_schema, metrics_schema, details_schema = report_tables_schema
    table_recon, source, target = mock_for_report_type_all

    with (
        patch("databricks.labs.remorph.reconcile.execute.datetime") as mock_datetime,
        patch("databricks.labs.remorph.reconcile.recon_capture.datetime") as recon_datetime,
        patch("databricks.labs.remorph.reconcile.execute.initialise_data_source", return_value=(source, target)),
        patch("databricks.labs.remorph.reconcile.execute.uuid4", return_value="00112233-4455-6677-8899-aabbccddeeff"),
        patch("databricks.labs.remorph.reconcile.recon_capture.ReconCapture._DB_PREFIX", new="default"),
        patch(
            "databricks.labs.remorph.reconcile.recon_capture.ReconCapture._generate_recon_main_id", return_value=33333
        ),
    ):
        mock_datetime.now.return_value = datetime(2024, 5, 23, 9, 21, 25, 122185)
        recon_datetime.now.return_value = datetime(2024, 5, 23, 9, 21, 25, 122185)
        recon_id = recon(mock_workspace_client, mock_spark, table_recon, get_dialect("snowflake"), "all")

    actual_remorph_recon = mock_spark.sql("SELECT * FROM DEFAULT.MAIN")
    actual_remorph_recon_metrics = mock_spark.sql("SELECT * FROM DEFAULT.METRICS")
    actual_remorph_recon_details = mock_spark.sql("SELECT * FROM DEFAULT.DETAILS")

    expected_remorph_recon = mock_spark.createDataFrame(
        data=[
            (
                33333,
                "00112233-4455-6677-8899-aabbccddeeff",
                "Snowflake",
                ("org", "data", "supplier"),
                ("org", "data", "target_supplier"),
                "all",
                datetime(2024, 5, 23, 9, 21, 25, 122185),
                datetime(2024, 5, 23, 9, 21, 25, 122185),
            )
        ],
        schema=recon_schema,
    )
    expected_remorph_recon_metrics = mock_spark.createDataFrame(
        data=[
            (
                33333,
                ((1, 1), (1, 0, "s_address,s_phone"), False),
                (False, "remorph", ""),
                datetime(2024, 5, 23, 9, 21, 25, 122185),
            )
        ],
        schema=metrics_schema,
    )
    expected_remorph_recon_details = mock_spark.createDataFrame(
        data=[
            (
                33333,
                "mismatch",
                False,
                [
                    {
                        "s_suppkey": "2",
                        "s_nationkey": "22",
                        "s_address_base": "address-2",
                        "s_address_compare": "address-22",
                        "s_address_match": "false",
                        "s_name_base": "name-2",
                        "s_name_compare": "name-2",
                        "s_name_match": "true",
                        "s_phone_base": "222-2",
                        "s_phone_compare": "222",
                        "s_phone_match": "false",
                    }
                ],
                datetime(2024, 5, 23, 9, 21, 25, 122185),
            ),
            (
                33333,
                "missing_in_source",
                False,
                [
                    {
                        "s_address": "address-4",
                        "s_name": "name-4",
                        "s_nationkey": "44",
                        "s_phone": "444",
                        "s_suppkey": "4",
                    }
                ],
                datetime(2024, 5, 23, 9, 21, 25, 122185),
            ),
            (
                33333,
                "missing_in_target",
                False,
                [
                    {
                        "s_address": "address-3",
                        "s_name": "name-3",
                        "s_nationkey": "33",
                        "s_phone": "333",
                        "s_suppkey": "3",
                    }
                ],
                datetime(2024, 5, 23, 9, 21, 25, 122185),
            ),
            (
                33333,
                "schema",
                False,
                [
                    {
                        "source_column": "s_suppkey",
                        "source_datatype": "number",
                        "databricks_column": "s_suppkey_t",
                        "databricks_datatype": "number",
                        "is_valid": "false",
                    },
                    {
                        "source_column": "s_name",
                        "source_datatype": "varchar",
                        "databricks_column": "s_name",
                        "databricks_datatype": "varchar",
                        "is_valid": "false",
                    },
                    {
                        "source_column": "s_address",
                        "source_datatype": "varchar",
                        "databricks_column": "s_address_t",
                        "databricks_datatype": "varchar",
                        "is_valid": "false",
                    },
                    {
                        "source_column": "s_nationkey",
                        "source_datatype": "number",
                        "databricks_column": "s_nationkey_t",
                        "databricks_datatype": "number",
                        "is_valid": "false",
                    },
                    {
                        "source_column": "s_phone",
                        "source_datatype": "varchar",
                        "databricks_column": "s_phone_t",
                        "databricks_datatype": "varchar",
                        "is_valid": "false",
                    },
                ],
                datetime(2024, 5, 23, 9, 21, 25, 122185),
            ),
        ],
        schema=details_schema,
    )

    assertDataFrameEqual(actual_remorph_recon, expected_remorph_recon, ignoreNullable=True)
    assertDataFrameEqual(actual_remorph_recon_metrics, expected_remorph_recon_metrics, ignoreNullable=True)
    assertDataFrameEqual(actual_remorph_recon_details, expected_remorph_recon_details, ignoreNullable=True)

    assert recon_id == "00112233-4455-6677-8899-aabbccddeeff"


@pytest.fixture
def mock_for_report_type_row(table_conf_with_opts, table_schema, mock_spark, query_store, setup_metadata_table):
    table_conf_with_opts.drop_columns = ["s_acctbal"]
    table_conf_with_opts.thresholds = None
    table_recon = TableRecon(
        source_catalog="org",
        source_schema="data",
        target_catalog="org",
        target_schema="data",
        tables=[table_conf_with_opts],
    )
    src_schema, tgt_schema = table_schema
    source_dataframe_repository = {
        (
            CATALOG,
            SCHEMA,
            query_store.source_row_query,
        ): mock_spark.createDataFrame(
            [
                Row(
                    hash_value_recon="a1b",
                    s_address="address-1",
                    s_name="name-1",
                    s_nationkey=11,
                    s_phone="111",
                    s_suppkey=1,
                ),
                Row(
                    hash_value_recon="c2d",
                    s_address="address-2",
                    s_name="name-2",
                    s_nationkey=22,
                    s_phone="222-2",
                    s_suppkey=2,
                ),
                Row(
                    hash_value_recon="e3g",
                    s_address="address-3",
                    s_name="name-3",
                    s_nationkey=33,
                    s_phone="333",
                    s_suppkey=3,
                ),
            ]
        ),
    }
    source_schema_repository = {(CATALOG, SCHEMA, SRC_TABLE): src_schema}

    target_dataframe_repository = {
        (
            CATALOG,
            SCHEMA,
            query_store.target_row_query,
        ): mock_spark.createDataFrame(
            [
                Row(
                    hash_value_recon="a1b",
                    s_address="address-1",
                    s_name="name-1",
                    s_nationkey=11,
                    s_phone="111",
                    s_suppkey=1,
                ),
                Row(
                    hash_value_recon="c2de",
                    s_address="address-2",
                    s_name="name-2",
                    s_nationkey=22,
                    s_phone="222",
                    s_suppkey=2,
                ),
                Row(
                    hash_value_recon="h4k",
                    s_address="address-4",
                    s_name="name-4",
                    s_nationkey=44,
                    s_phone="444",
                    s_suppkey=4,
                ),
            ]
        )
    }

    target_schema_repository = {(CATALOG, SCHEMA, TGT_TABLE): tgt_schema}
    source = MockDataSource(source_dataframe_repository, source_schema_repository)
    target = MockDataSource(target_dataframe_repository, target_schema_repository)

    return source, target, table_recon


def test_recon_for_report_type_is_row(
    mock_workspace_client, mock_spark, mock_for_report_type_row, report_tables_schema
):
    recon_schema, metrics_schema, details_schema = report_tables_schema
    source, target, table_recon = mock_for_report_type_row
    with (
        patch("databricks.labs.remorph.reconcile.execute.datetime") as mock_datetime,
        patch("databricks.labs.remorph.reconcile.recon_capture.datetime") as recon_datetime,
        patch("databricks.labs.remorph.reconcile.execute.initialise_data_source", return_value=(source, target)),
        patch("databricks.labs.remorph.reconcile.execute.uuid4", return_value="00112233-4455-6677-8899-aabbccddeeff"),
        patch("databricks.labs.remorph.reconcile.recon_capture.ReconCapture._DB_PREFIX", new="default"),
        patch(
            "databricks.labs.remorph.reconcile.recon_capture.ReconCapture._generate_recon_main_id", return_value=33333
        ),
    ):
        mock_datetime.now.return_value = datetime(2024, 5, 23, 9, 21, 25, 122185)
        recon_datetime.now.return_value = datetime(2024, 5, 23, 9, 21, 25, 122185)
        recon_id = recon(mock_workspace_client, mock_spark, table_recon, get_dialect("snowflake"), "row")

    actual_remorph_recon = mock_spark.sql("SELECT * FROM DEFAULT.MAIN")
    actual_remorph_recon_metrics = mock_spark.sql("SELECT * FROM DEFAULT.METRICS")
    actual_remorph_recon_details = mock_spark.sql("SELECT * FROM DEFAULT.DETAILS")

    expected_remorph_recon = mock_spark.createDataFrame(
        data=[
            (
                33333,
                "00112233-4455-6677-8899-aabbccddeeff",
                "Snowflake",
                ("org", "data", "supplier"),
                ("org", "data", "target_supplier"),
                "row",
                datetime(2024, 5, 23, 9, 21, 25, 122185),
                datetime(2024, 5, 23, 9, 21, 25, 122185),
            )
        ],
        schema=recon_schema,
    )
    expected_remorph_recon_metrics = mock_spark.createDataFrame(
        data=[
            (
                33333,
                ((2, 2), (0, 0, ""), True),
                (False, "remorph", ""),
                datetime(2024, 5, 23, 9, 21, 25, 122185),
            )
        ],
        schema=metrics_schema,
    )
    expected_remorph_recon_details = mock_spark.createDataFrame(
        data=[
            (
                33333,
                "missing_in_source",
                False,
                [
                    {
                        's_address': 'address-2',
                        's_name': 'name-2',
                        's_nationkey': '22',
                        's_phone': '222',
                        's_suppkey': '2',
                    },
                    {
                        's_address': 'address-4',
                        's_name': 'name-4',
                        's_nationkey': '44',
                        's_phone': '444',
                        's_suppkey': '4',
                    },
                ],
                datetime(2024, 5, 23, 9, 21, 25, 122185),
            ),
            (
                33333,
                "missing_in_target",
                False,
                [
                    {
                        's_address': 'address-2',
                        's_name': 'name-2',
                        's_nationkey': '22',
                        's_phone': '222-2',
                        's_suppkey': '2',
                    },
                    {
                        's_address': 'address-3',
                        's_name': 'name-3',
                        's_nationkey': '33',
                        's_phone': '333',
                        's_suppkey': '3',
                    },
                ],
                datetime(2024, 5, 23, 9, 21, 25, 122185),
            ),
        ],
        schema=details_schema,
    )

    assertDataFrameEqual(actual_remorph_recon, expected_remorph_recon, ignoreNullable=True)
    assertDataFrameEqual(actual_remorph_recon_metrics, expected_remorph_recon_metrics, ignoreNullable=True)
    assertDataFrameEqual(actual_remorph_recon_details, expected_remorph_recon_details, ignoreNullable=True)

    assert recon_id == "00112233-4455-6677-8899-aabbccddeeff"


@pytest.fixture
def mock_for_recon_exception(table_conf_with_opts, setup_metadata_table):
    table_conf_with_opts.drop_columns = ["s_acctbal"]
    table_conf_with_opts.thresholds = None
    table_conf_with_opts.join_columns = None
    table_recon = TableRecon(
        source_catalog="org",
        source_schema="data",
        target_catalog="org",
        target_schema="data",
        tables=[table_conf_with_opts],
    )
    source = MockDataSource({}, {})
    target = MockDataSource({}, {})

    return table_recon, source, target


def test_schema_recon_with_data_source_exception(
    mock_workspace_client, mock_spark, report_tables_schema, mock_for_recon_exception
):
    recon_schema, metrics_schema, details_schema = report_tables_schema
    table_recon, source, target = mock_for_recon_exception
    with (
        patch("databricks.labs.remorph.reconcile.execute.datetime") as mock_datetime,
        patch("databricks.labs.remorph.reconcile.recon_capture.datetime") as recon_datetime,
        patch("databricks.labs.remorph.reconcile.execute.initialise_data_source", return_value=(source, target)),
        patch("databricks.labs.remorph.reconcile.execute.uuid4", return_value="00112233-4455-6677-8899-aabbccddeeff"),
        patch("databricks.labs.remorph.reconcile.recon_capture.ReconCapture._DB_PREFIX", new="default"),
        patch(
            "databricks.labs.remorph.reconcile.recon_capture.ReconCapture._generate_recon_main_id", return_value=33333
        ),
    ):
        mock_datetime.now.return_value = datetime(2024, 5, 23, 9, 21, 25, 122185)
        recon_datetime.now.return_value = datetime(2024, 5, 23, 9, 21, 25, 122185)
        recon_id = recon(mock_workspace_client, mock_spark, table_recon, get_dialect("snowflake"), "all")

    actual_remorph_recon = mock_spark.sql("SELECT * FROM DEFAULT.MAIN")
    actual_remorph_recon_metrics = mock_spark.sql("SELECT * FROM DEFAULT.METRICS")
    actual_remorph_recon_details = mock_spark.sql("SELECT * FROM DEFAULT.DETAILS")

    expected_remorph_recon = mock_spark.createDataFrame(
        data=[
            (
                33333,
                "00112233-4455-6677-8899-aabbccddeeff",
                "Snowflake",
                ("org", "data", "supplier"),
                ("org", "data", "target_supplier"),
                "all",
                datetime(2024, 5, 23, 9, 21, 25, 122185),
                datetime(2024, 5, 23, 9, 21, 25, 122185),
            )
        ],
        schema=recon_schema,
    )
    expected_remorph_recon_metrics = mock_spark.createDataFrame(
        data=[
            (
                33333,
                ((0, 0), (0, 0, ""), True),
                (
                    False,
                    "remorph",
                    "Runtime exception occurred while fetching schema using (org, data, supplier) : Mock Exception",
                ),
                datetime(2024, 5, 23, 9, 21, 25, 122185),
            )
        ],
        schema=metrics_schema,
    )
    expected_remorph_recon_details = mock_spark.createDataFrame(data=[], schema=details_schema)

    assertDataFrameEqual(actual_remorph_recon, expected_remorph_recon, ignoreNullable=True)
    assertDataFrameEqual(actual_remorph_recon_metrics, expected_remorph_recon_metrics, ignoreNullable=True)
    assertDataFrameEqual(actual_remorph_recon_details, expected_remorph_recon_details, ignoreNullable=True)

    assert recon_id == "00112233-4455-6677-8899-aabbccddeeff"


def test_schema_recon_with_general_exception(
    mock_workspace_client, mock_spark, report_tables_schema, mock_for_report_type_schema
):
    recon_schema, metrics_schema, details_schema = report_tables_schema
    table_recon, source, target = mock_for_report_type_schema
    with (
        patch("databricks.labs.remorph.reconcile.execute.datetime") as mock_datetime,
        patch("databricks.labs.remorph.reconcile.recon_capture.datetime") as recon_datetime,
        patch("databricks.labs.remorph.reconcile.execute.initialise_data_source", return_value=(source, target)),
        patch("databricks.labs.remorph.reconcile.execute.uuid4", return_value="00112233-4455-6677-8899-aabbccddeeff"),
        patch("databricks.labs.remorph.reconcile.recon_capture.ReconCapture._DB_PREFIX", new="default"),
        patch(
            "databricks.labs.remorph.reconcile.recon_capture.ReconCapture._generate_recon_main_id", return_value=33333
        ),
        patch("databricks.labs.remorph.reconcile.execute.Reconciliation.reconcile_schema") as schema_source_mock,
    ):
        schema_source_mock.side_effect = PySparkException("Unknown Error")
        mock_datetime.now.return_value = datetime(2024, 5, 23, 9, 21, 25, 122185)
        recon_datetime.now.return_value = datetime(2024, 5, 23, 9, 21, 25, 122185)
        recon_id = recon(mock_workspace_client, mock_spark, table_recon, get_dialect("snowflake"), "schema")

    expected_remorph_recon = mock_spark.createDataFrame(
        data=[
            (
                33333,
                "00112233-4455-6677-8899-aabbccddeeff",
                "Snowflake",
                ("org", "data", "supplier"),
                ("org", "data", "target_supplier"),
                "schema",
                datetime(2024, 5, 23, 9, 21, 25, 122185),
                datetime(2024, 5, 23, 9, 21, 25, 122185),
            )
        ],
        schema=recon_schema,
    )
    expected_remorph_recon_metrics = mock_spark.createDataFrame(
        data=[
            (
                33333,
                ((0, 0), (0, 0, ""), False),
                (
                    False,
                    "remorph",
                    "Unknown Error",
                ),
                datetime(2024, 5, 23, 9, 21, 25, 122185),
            )
        ],
        schema=metrics_schema,
    )
    expected_remorph_recon_details = mock_spark.createDataFrame(data=[], schema=details_schema)

    assertDataFrameEqual(mock_spark.sql("SELECT * FROM DEFAULT.MAIN"), expected_remorph_recon, ignoreNullable=True)
    assertDataFrameEqual(
        mock_spark.sql("SELECT * FROM DEFAULT.METRICS"), expected_remorph_recon_metrics, ignoreNullable=True
    )
    assertDataFrameEqual(
        mock_spark.sql("SELECT * FROM DEFAULT.DETAILS"), expected_remorph_recon_details, ignoreNullable=True
    )

    assert recon_id == "00112233-4455-6677-8899-aabbccddeeff"


def test_data_recon_with_general_exception(
    mock_workspace_client, mock_spark, report_tables_schema, mock_for_report_type_schema
):
    recon_schema, metrics_schema, details_schema = report_tables_schema
    table_recon, source, target = mock_for_report_type_schema
    with (
        patch("databricks.labs.remorph.reconcile.execute.datetime") as mock_datetime,
        patch("databricks.labs.remorph.reconcile.recon_capture.datetime") as recon_datetime,
        patch("databricks.labs.remorph.reconcile.execute.initialise_data_source", return_value=(source, target)),
        patch("databricks.labs.remorph.reconcile.execute.uuid4", return_value="00112233-4455-6677-8899-aabbccddeeff"),
        patch("databricks.labs.remorph.reconcile.recon_capture.ReconCapture._DB_PREFIX", new="default"),
        patch(
            "databricks.labs.remorph.reconcile.recon_capture.ReconCapture._generate_recon_main_id", return_value=33333
        ),
        patch("databricks.labs.remorph.reconcile.execute.Reconciliation.reconcile_data") as data_source_mock,
    ):
        data_source_mock.side_effect = PySparkException("Unknown Error")
        mock_datetime.now.return_value = datetime(2024, 5, 23, 9, 21, 25, 122185)
        recon_datetime.now.return_value = datetime(2024, 5, 23, 9, 21, 25, 122185)
        recon_id = recon(mock_workspace_client, mock_spark, table_recon, get_dialect("snowflake"), "data")

    expected_remorph_recon = mock_spark.createDataFrame(
        data=[
            (
                33333,
                "00112233-4455-6677-8899-aabbccddeeff",
                "Snowflake",
                ("org", "data", "supplier"),
                ("org", "data", "target_supplier"),
                "data",
                datetime(2024, 5, 23, 9, 21, 25, 122185),
                datetime(2024, 5, 23, 9, 21, 25, 122185),
            )
        ],
        schema=recon_schema,
    )
    expected_remorph_recon_metrics = mock_spark.createDataFrame(
        data=[
            (
                33333,
                ((0, 0), (0, 0, ""), True),
                (
                    False,
                    "remorph",
                    "Unknown Error",
                ),
                datetime(2024, 5, 23, 9, 21, 25, 122185),
            )
        ],
        schema=metrics_schema,
    )
    expected_remorph_recon_details = mock_spark.createDataFrame(data=[], schema=details_schema)

    assertDataFrameEqual(mock_spark.sql("SELECT * FROM DEFAULT.MAIN"), expected_remorph_recon, ignoreNullable=True)
    assertDataFrameEqual(
        mock_spark.sql("SELECT * FROM DEFAULT.METRICS"), expected_remorph_recon_metrics, ignoreNullable=True
    )
    assertDataFrameEqual(
        mock_spark.sql("SELECT * FROM DEFAULT.DETAILS"), expected_remorph_recon_details, ignoreNullable=True
    )

    assert recon_id == "00112233-4455-6677-8899-aabbccddeeff"


def test_data_recon_with_source_exception(
    mock_workspace_client, mock_spark, report_tables_schema, mock_for_report_type_schema
):
    recon_schema, metrics_schema, details_schema = report_tables_schema
    table_recon, source, target = mock_for_report_type_schema
    with (
        patch("databricks.labs.remorph.reconcile.execute.datetime") as mock_datetime,
        patch("databricks.labs.remorph.reconcile.recon_capture.datetime") as recon_datetime,
        patch("databricks.labs.remorph.reconcile.execute.initialise_data_source", return_value=(source, target)),
        patch("databricks.labs.remorph.reconcile.execute.uuid4", return_value="00112233-4455-6677-8899-aabbccddeeff"),
        patch("databricks.labs.remorph.reconcile.recon_capture.ReconCapture._DB_PREFIX", new="default"),
        patch(
            "databricks.labs.remorph.reconcile.recon_capture.ReconCapture._generate_recon_main_id", return_value=33333
        ),
        patch("databricks.labs.remorph.reconcile.execute.Reconciliation.reconcile_data") as data_source_mock,
    ):
        data_source_mock.side_effect = DataSourceRuntimeException("Source Runtime Error")
        mock_datetime.now.return_value = datetime(2024, 5, 23, 9, 21, 25, 122185)
        recon_datetime.now.return_value = datetime(2024, 5, 23, 9, 21, 25, 122185)
        recon_id = recon(mock_workspace_client, mock_spark, table_recon, get_dialect("snowflake"), "data")

    expected_remorph_recon = mock_spark.createDataFrame(
        data=[
            (
                33333,
                "00112233-4455-6677-8899-aabbccddeeff",
                "Snowflake",
                ("org", "data", "supplier"),
                ("org", "data", "target_supplier"),
                "data",
                datetime(2024, 5, 23, 9, 21, 25, 122185),
                datetime(2024, 5, 23, 9, 21, 25, 122185),
            )
        ],
        schema=recon_schema,
    )
    expected_remorph_recon_metrics = mock_spark.createDataFrame(
        data=[
            (
                33333,
                ((0, 0), (0, 0, ""), True),
                (
                    False,
                    "remorph",
                    "Source Runtime Error",
                ),
                datetime(2024, 5, 23, 9, 21, 25, 122185),
            )
        ],
        schema=metrics_schema,
    )
    expected_remorph_recon_details = mock_spark.createDataFrame(data=[], schema=details_schema)

    assertDataFrameEqual(mock_spark.sql("SELECT * FROM DEFAULT.MAIN"), expected_remorph_recon, ignoreNullable=True)
    assertDataFrameEqual(
        mock_spark.sql("SELECT * FROM DEFAULT.METRICS"), expected_remorph_recon_metrics, ignoreNullable=True
    )
    assertDataFrameEqual(
        mock_spark.sql("SELECT * FROM DEFAULT.DETAILS"), expected_remorph_recon_details, ignoreNullable=True
    )

    assert recon_id == "00112233-4455-6677-8899-aabbccddeeff"


def test__initialise_data_source(mock_workspace_client, mock_spark):
    src_engine = get_dialect("snowflake")
    secret_scope = "test"

    source, target = initialise_data_source(mock_workspace_client, mock_spark, src_engine, secret_scope)

    snowflake_data_source = SnowflakeDataSource(src_engine, mock_spark, mock_workspace_client, secret_scope).__class__
    databricks_data_source = DatabricksDataSource(src_engine, mock_spark, mock_workspace_client, secret_scope).__class__

    assert isinstance(source, snowflake_data_source)
    assert isinstance(target, databricks_data_source)
