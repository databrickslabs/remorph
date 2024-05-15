from dataclasses import dataclass
from unittest.mock import create_autospec, patch

import pytest
from pyspark import Row
from pyspark.testing import assertDataFrameEqual

from databricks.connect import DatabricksSession
from databricks.labs.remorph.config import SQLGLOT_DIALECTS, DatabaseConfig, TableRecon
from databricks.labs.remorph.reconcile.connectors.data_source import MockDataSource
from databricks.labs.remorph.reconcile.execute import Reconciliation, recon
from databricks.labs.remorph.reconcile.recon_config import (
    MismatchOutput,
    ReconcileOutput,
)
from databricks.labs.remorph.reconcile.schema_compare import SchemaCompare

CATALOG = "org"
SCHEMA = "data"
TABLE = "supplier"


@dataclass
class QueryStore:
    source_hash_query: str
    target_hash_query: str
    source_mismatch_query: str
    target_mismatch_query: str
    source_missing_query: str
    target_missing_query: str


@pytest.fixture
def query_store():
    source_hash_query = "SELECT LOWER(SHA2(CONCAT(TRIM(s_address), TRIM(s_name), COALESCE(TRIM(s_nationkey), ''), TRIM(s_phone), COALESCE(TRIM(s_suppkey), '')), 256)) AS hash_value_recon, COALESCE(TRIM(s_nationkey), '') AS s_nationkey, COALESCE(TRIM(s_suppkey), '') AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address = 'a'"
    target_hash_query = "SELECT LOWER(SHA2(CONCAT(TRIM(s_address_t), TRIM(s_name), COALESCE(TRIM(s_nationkey_t), ''), TRIM(s_phone_t), COALESCE(TRIM(s_suppkey_t), '')), 256)) AS hash_value_recon, COALESCE(TRIM(s_nationkey_t), '') AS s_nationkey, COALESCE(TRIM(s_suppkey_t), '') AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address_t = 'a'"
    source_mismatch_query = "WITH recon AS (SELECT 22 AS s_nationkey, 2 AS s_suppkey), src AS (SELECT TRIM(s_address) AS s_address, TRIM(s_name) AS s_name, COALESCE(TRIM(s_nationkey), '') AS s_nationkey, TRIM(s_phone) AS s_phone, COALESCE(TRIM(s_suppkey), '') AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address = 'a') SELECT s_address, s_name, s_nationkey, s_phone, s_suppkey FROM src INNER JOIN recon USING (s_nationkey, s_suppkey)"
    target_mismatch_query = "WITH recon AS (SELECT 22 AS s_nationkey, 2 AS s_suppkey), src AS (SELECT TRIM(s_address_t) AS s_address, TRIM(s_name) AS s_name, COALESCE(TRIM(s_nationkey_t), '') AS s_nationkey, TRIM(s_phone_t) AS s_phone, COALESCE(TRIM(s_suppkey_t), '') AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address_t = 'a') SELECT s_address, s_name, s_nationkey, s_phone, s_suppkey FROM src INNER JOIN recon USING (s_nationkey, s_suppkey)"
    source_missing_query = "WITH recon AS (SELECT 44 AS s_nationkey, 4 AS s_suppkey), src AS (SELECT TRIM(s_address_t) AS s_address, TRIM(s_name) AS s_name, COALESCE(TRIM(s_nationkey_t), '') AS s_nationkey, TRIM(s_phone_t) AS s_phone, COALESCE(TRIM(s_suppkey_t), '') AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address_t = 'a') SELECT s_address, s_name, s_nationkey, s_phone, s_suppkey FROM src INNER JOIN recon USING (s_nationkey, s_suppkey)"
    target_missing_query = "WITH recon AS (SELECT 33 AS s_nationkey, 3 AS s_suppkey), src AS (SELECT TRIM(s_address) AS s_address, TRIM(s_name) AS s_name, COALESCE(TRIM(s_nationkey), '') AS s_nationkey, TRIM(s_phone) AS s_phone, COALESCE(TRIM(s_suppkey), '') AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address = 'a') SELECT s_address, s_name, s_nationkey, s_phone, s_suppkey FROM src INNER JOIN recon USING (s_nationkey, s_suppkey)"

    return QueryStore(
        source_hash_query=source_hash_query,
        target_hash_query=target_hash_query,
        source_mismatch_query=source_mismatch_query,
        target_mismatch_query=target_mismatch_query,
        source_missing_query=source_missing_query,
        target_missing_query=target_missing_query,
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
            [Row(s_address='address-2', s_name='name-2', s_nationkey=22, s_phone="222-2", s_suppkey=2)]
        ),
        (CATALOG, SCHEMA, query_store.target_missing_query): mock_spark.createDataFrame(
            [Row(s_address='address-3', s_name='name-3', s_nationkey=33, s_phone="333", s_suppkey=3)]
        ),
    }
    source_schema_repository = {(CATALOG, SCHEMA, TABLE): src_schema}

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
            [Row(s_address='address-22', s_name='name-2', s_nationkey=22, s_phone="222", s_suppkey=2)]
        ),
        (CATALOG, SCHEMA, query_store.source_missing_query): mock_spark.createDataFrame(
            [Row(s_address='address-4', s_name='name-4', s_nationkey=44, s_phone="444", s_suppkey=4)]
        ),
    }

    target_schema_repository = {(CATALOG, SCHEMA, TABLE): tgt_schema}
    database_config = DatabaseConfig(
        source_catalog=CATALOG,
        source_schema=SCHEMA,
        target_catalog=CATALOG,
        target_schema=SCHEMA,
    )
    schema_comparator = SchemaCompare(mock_spark)
    source = MockDataSource(source_dataframe_repository, source_schema_repository)
    target = MockDataSource(target_dataframe_repository, target_schema_repository)
    reconciler = Reconciliation(
        source, target, database_config, "data", schema_comparator, SQLGLOT_DIALECTS.get("databricks")
    )
    actual_data_reconcile = reconciler.reconcile_data(table_conf_with_opts, src_schema, tgt_schema)
    expected_data_reconcile = ReconcileOutput(
        mismatch_count=1,
        missing_in_src_count=1,
        missing_in_tgt_count=1,
        missing_in_src=mock_spark.createDataFrame(
            [Row(s_address='address-4', s_name='name-4', s_nationkey=44, s_phone="444", s_suppkey=4)]
        ),
        missing_in_tgt=mock_spark.createDataFrame(
            [Row(s_address='address-3', s_name='name-3', s_nationkey=33, s_phone="333", s_suppkey=3)]
        ),
        mismatch=MismatchOutput(
            mismatch_df=mock_spark.createDataFrame(
                [
                    Row(
                        s_suppkey=2,
                        s_nationkey=22,
                        s_address_base='address-2',
                        s_address_compare='address-22',
                        s_address_match=False,
                        s_name_base='name-2',
                        s_name_compare='name-2',
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


def test_reconcile_data_without_mismatches_and_missing(mock_spark, table_conf_with_opts, table_schema, query_store):
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
    }
    source_schema_repository = {(CATALOG, SCHEMA, TABLE): src_schema}

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
    }

    target_schema_repository = {(CATALOG, SCHEMA, TABLE): tgt_schema}
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
        source, target, database_config, "data", schema_comparator, SQLGLOT_DIALECTS.get("databricks")
    ).reconcile_data(table_conf_with_opts, src_schema, tgt_schema)

    assert actual.mismatch_count == 0
    assert actual.missing_in_src_count == 0
    assert actual.missing_in_tgt_count == 0
    assert actual.mismatch is None
    assert actual.missing_in_src is None
    assert actual.missing_in_tgt is None


def test_reconcile_data_with_mismatch_and_no_missing(mock_spark, table_conf_with_opts, table_schema, query_store):
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
        (CATALOG, SCHEMA, query_store.source_mismatch_query): mock_spark.createDataFrame(
            [Row(s_address='address-2', s_name='name-2', s_nationkey=22, s_phone="222-2", s_suppkey=2)]
        ),
    }
    source_schema_repository = {(CATALOG, SCHEMA, TABLE): src_schema}

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
            [Row(s_address='address-22', s_name='name-2', s_nationkey=22, s_phone="222", s_suppkey=2)]
        ),
    }

    target_schema_repository = {(CATALOG, SCHEMA, TABLE): tgt_schema}
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
        source, target, database_config, "data", schema_comparator, SQLGLOT_DIALECTS.get("databricks")
    ).reconcile_data(table_conf_with_opts, src_schema, tgt_schema)
    expected = ReconcileOutput(
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
                        s_address_base='address-2',
                        s_address_compare='address-22',
                        s_address_match=False,
                        s_name_base='name-2',
                        s_name_compare='name-2',
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
            [Row(s_address='address-3', s_name='name-3', s_nationkey=33, s_phone="333", s_suppkey=3)]
        ),
    }
    source_schema_repository = {(CATALOG, SCHEMA, TABLE): src_schema}

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
            [Row(s_address='address-4', s_name='name-4', s_nationkey=44, s_phone="444", s_suppkey=4)]
        ),
    }

    target_schema_repository = {(CATALOG, SCHEMA, TABLE): tgt_schema}
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
        source, target, database_config, "data", schema_comparator, SQLGLOT_DIALECTS.get("databricks")
    ).reconcile_data(table_conf_with_opts, src_schema, tgt_schema)
    expected = ReconcileOutput(
        mismatch_count=0,
        missing_in_src_count=1,
        missing_in_tgt_count=1,
        missing_in_src=mock_spark.createDataFrame(
            [Row(s_address='address-4', s_name='name-4', s_nationkey=44, s_phone="444", s_suppkey=4)]
        ),
        missing_in_tgt=mock_spark.createDataFrame(
            [Row(s_address='address-3', s_name='name-3', s_nationkey=33, s_phone="333", s_suppkey=3)]
        ),
        mismatch=None,
    )

    assert actual.mismatch_count == expected.mismatch_count
    assert actual.missing_in_src_count == expected.missing_in_src_count
    assert actual.missing_in_tgt_count == expected.missing_in_tgt_count
    assert actual.mismatch is None

    assertDataFrameEqual(actual.missing_in_src, expected.missing_in_src)
    assertDataFrameEqual(actual.missing_in_tgt, expected.missing_in_tgt)


def test_recon(mock_workspace_client, table_conf_with_opts, table_schema, mock_spark, query_store):
    table_recon = TableRecon(
        source_catalog="org",
        source_schema="data",
        target_catalog="org",
        target_schema='data',
        tables=[table_conf_with_opts],
    )
    spark = create_autospec(DatabricksSession)
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
            [Row(s_address='address-2', s_name='name-2', s_nationkey=22, s_phone="222-2", s_suppkey=2)]
        ),
        (CATALOG, SCHEMA, query_store.target_missing_query): mock_spark.createDataFrame(
            [Row(s_address='address-3', s_name='name-3', s_nationkey=33, s_phone="333", s_suppkey=3)]
        ),
    }
    source_schema_repository = {(CATALOG, SCHEMA, TABLE): src_schema}

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
            [Row(s_address='address-22', s_name='name-2', s_nationkey=22, s_phone="222", s_suppkey=2)]
        ),
        (CATALOG, SCHEMA, query_store.source_missing_query): mock_spark.createDataFrame(
            [Row(s_address='address-4', s_name='name-4', s_nationkey=44, s_phone="444", s_suppkey=4)]
        ),
    }

    target_schema_repository = {(CATALOG, SCHEMA, TABLE): tgt_schema}
    source = MockDataSource(source_dataframe_repository, source_schema_repository)
    target = MockDataSource(target_dataframe_repository, target_schema_repository)

    with (
        patch("databricks.labs.remorph.reconcile.execute._initialise_data_source", return_value=(source, target)),
        patch(
            "databricks.labs.remorph.reconcile.execute.uuid.uuid4", return_value="00112233-4455-6677-8899-aabbccddeeff"
        ),
    ):
        recon_id = recon(mock_workspace_client, spark, table_recon, SQLGLOT_DIALECTS.get("databricks"), "data")

    assert recon_id == "00112233-4455-6677-8899-aabbccddeeff"
