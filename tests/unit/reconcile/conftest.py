import pytest
from pyspark.sql import SparkSession
from sqlglot import parse_one

from databricks.labs.remorph.reconcile.recon_config import (
    ColumnMapping,
    Filters,
    JdbcReaderOptions,
    Schema,
    Table,
    Thresholds,
    Transformation,
)


@pytest.fixture
def mock_spark_session() -> SparkSession:
    """
    Method helps to create spark session
    :return: returns the spark session
    """
    return (
        SparkSession.builder.master("local[*]").appName("Remorph Reconcile Test").remote("sc://localhost").getOrCreate()
    )


@pytest.fixture
def table_conf_mock():
    def _mock_table_conf(**kwargs):
        return Table(
            source_name="supplier",
            target_name="supplier",
            jdbc_reader_options=kwargs.get('jdbc_reader_options', None),
            join_columns=kwargs.get('join_columns', None),
            select_columns=kwargs.get('select_columns', None),
            drop_columns=kwargs.get('drop_columns', None),
            column_mapping=kwargs.get('column_mapping', None),
            transformations=kwargs.get('transformations', None),
            thresholds=kwargs.get('thresholds', None),
            filters=kwargs.get('filters', None),
        )

    return _mock_table_conf


@pytest.fixture
def table_conf_with_opts(column_mapping):
    return Table(
        source_name="supplier",
        target_name="target_supplier",
        jdbc_reader_options=JdbcReaderOptions(
            number_partitions=100, partition_column="s_nationkey", lower_bound="0", upper_bound="100"
        ),
        join_columns=["s_suppkey", "s_nationkey"],
        select_columns=["s_suppkey", "s_name", "s_address", "s_phone", "s_acctbal", "s_nationkey"],
        drop_columns=["s_comment"],
        column_mapping=column_mapping,
        transformations=[
            Transformation(column_name="s_address", source="trim(s_address)", target="trim(s_address_t)"),
            Transformation(column_name="s_phone", source="trim(s_phone)", target="trim(s_phone_t)"),
            Transformation(column_name="s_name", source="trim(s_name)", target="trim(s_name)"),
        ],
        thresholds=[Thresholds(column_name="s_acctbal", lower_bound="0", upper_bound="100", type="int")],
        filters=Filters(source="s_name='t' and s_address='a'", target="s_name='t' and s_address_t='a'"),
    )


@pytest.fixture
def column_mapping():
    return [
        ColumnMapping(source_name="s_suppkey", target_name="s_suppkey_t"),
        ColumnMapping(source_name="s_address", target_name="s_address_t"),
        ColumnMapping(source_name="s_nationkey", target_name="s_nationkey_t"),
        ColumnMapping(source_name="s_phone", target_name="s_phone_t"),
        ColumnMapping(source_name="s_acctbal", target_name="s_acctbal_t"),
        ColumnMapping(source_name="s_comment", target_name="s_comment_t"),
    ]


@pytest.fixture
def schema():
    sch = [
        Schema("s_suppkey", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address", "varchar"),
        Schema("s_nationkey", "number"),
        Schema("s_phone", "varchar"),
        Schema("s_acctbal", "number"),
        Schema("s_comment", "varchar"),
    ]

    sch_with_alias = [
        Schema("s_suppkey_t", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address_t", "varchar"),
        Schema("s_nationkey_t", "number"),
        Schema("s_phone_t", "varchar"),
        Schema("s_acctbal_t", "number"),
        Schema("s_comment_t", "varchar"),
    ]

    return sch, sch_with_alias


@pytest.fixture
def expr():
    return parse_one("SELECT col1 FROM DUAL")
