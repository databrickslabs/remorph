import pytest
from pyspark.sql import SparkSession

from databricks.labs.remorph.reconcile.recon_config import Table, Schema


@pytest.fixture
def mock_spark_session() -> SparkSession:
    """
    Method helps to create spark session
    :return: returns the spark session
    """
    return (SparkSession.builder
            .master("local[*]")
            .appName("Remorph Reconcile Test")
            .remote("sc://localhost")
            .getOrCreate()
            )


@pytest.fixture
def table_conf():
    def _mock_table_conf(**kwargs):
        return Table(
            source_name="supplier",
            target_name="target_supplier",
            jdbc_reader_options=kwargs.get('jdbc_reader_options', None),
            join_columns=kwargs.get('join_columns', None),
            select_columns=kwargs.get('select_columns', None),
            drop_columns=kwargs.get('drop_columns', None),
            column_mapping=kwargs.get('column_mapping', None),
            transformations=kwargs.get('transformations', None),
            thresholds=kwargs.get('thresholds', None),
            filters=kwargs.get('filters', None)
        )

    return _mock_table_conf


@pytest.fixture
def source_schema():
    return [
        Schema("s_suppkey", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address", "varchar"),
        Schema("s_nationkey", "number"),
        Schema("s_phone", "varchar"),
        Schema("s_acctbal", "number"),
        Schema("s_comment", "varchar"),
    ]


@pytest.fixture
def target_schema():
    return [
        Schema("s_suppkey_t", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address_t", "varchar"),
        Schema("s_nationkey_t", "number"),
        Schema("s_phone_t", "varchar"),
        Schema("s_acctbal_t", "number"),
        Schema("s_comment_t", "varchar"),
    ]
