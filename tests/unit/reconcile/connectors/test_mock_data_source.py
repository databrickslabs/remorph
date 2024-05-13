import pytest
from pyspark import Row
from pyspark.testing import assertDataFrameEqual

from databricks.labs.remorph.reconcile.connectors.data_source import MockDataSource
from databricks.labs.remorph.reconcile.exception import MockDataNotAvailableException
from databricks.labs.remorph.reconcile.recon_config import Schema

catalog = "org"
schema = "data"
table = "employee"


def test_mock_data_source_happy(mock_spark):
    dataframe_repository = {
        (
            "org",
            "data",
            "select * from employee",
        ): mock_spark.createDataFrame(
            [
                Row(emp_id="1", emp_name="name-1", sal=100),
                Row(emp_id="2", emp_name="name-2", sal=200),
                Row(emp_id="3", emp_name="name-3", sal=300),
            ]
        )
    }
    schema_repository = {
        (catalog, schema, table): [
            Schema(column_name="emp_id", data_type="int"),
            Schema(column_name="emp_name", data_type="str"),
            Schema(column_name="sal", data_type="int"),
        ]
    }

    data_source = MockDataSource(dataframe_repository, schema_repository)

    actual_data = data_source.read_query_data(catalog, schema, table, "select * from employee", None)
    expected_data = mock_spark.createDataFrame(
        [
            Row(emp_id="1", emp_name="name-1", sal=100),
            Row(emp_id="2", emp_name="name-2", sal=200),
            Row(emp_id="3", emp_name="name-3", sal=300),
        ]
    )

    actual_schema = data_source.get_schema(catalog, schema, table)
    assertDataFrameEqual(actual_data, expected_data)
    assert actual_schema == [
        Schema(column_name="emp_id", data_type="int"),
        Schema(column_name="emp_name", data_type="str"),
        Schema(column_name="sal", data_type="int"),
    ]


def test_mock_data_source_fail(mock_spark):
    data_source = MockDataSource({}, {})

    with pytest.raises(MockDataNotAvailableException) as exception:
        data_source.read_query_data(catalog, schema, table, "select * from test", None)
    assert str(exception.value) == "data is not mocked for the combination : ('org', 'data', 'select * from test')"

    with pytest.raises(MockDataNotAvailableException) as exception:
        data_source.get_schema(catalog, schema, "unknown")
    assert str(exception.value) == "schema is not mocked for the combination : ('org', 'data', 'unknown')"
