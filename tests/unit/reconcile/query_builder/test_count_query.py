import pytest

from databricks.labs.lakebridge.reconcile.query_builder.query_builder import QueryBuilder
from databricks.labs.lakebridge.reconcile.recon_config import Layer


@pytest.mark.parametrize(
    "layer, dialect, expected",
    [
        (Layer.SOURCE, "oracle", "SELECT COUNT(1) AS count FROM :tbl WHERE s_name = 't' AND s_address = 'a'"),
        (Layer.TARGET, "databricks", "SELECT COUNT(1) AS count FROM :tbl WHERE s_name = 't' AND s_address_t = 'a'"),
    ],
)
def test_count_query(table_mapping_with_opts, layer, dialect, expected):
    # no column types required for count query
    builder = QueryBuilder.for_dialect(table_mapping_with_opts, [], layer, dialect)
    query = builder.build_count_query()
    assert query == expected
