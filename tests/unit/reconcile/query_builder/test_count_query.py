from databricks.labs.remorph.reconcile.dialects.utils import get_dialect
from databricks.labs.remorph.reconcile.query_builder.count_query import CountQueryBuilder


def test_count_query_sqlglot(table_conf_with_opts):
    source_query = CountQueryBuilder(
        table=table_conf_with_opts, layer="source", dialect=get_dialect("oracle")
    ).build_query()
    target_query = CountQueryBuilder(
        table=table_conf_with_opts, layer="target", dialect=get_dialect("databricks")
    ).build_query()
    assert source_query == "SELECT COUNT(1) AS count FROM :tbl WHERE s_name = 't' AND s_address = 'a'"
    assert target_query == "SELECT COUNT(1) AS count FROM :tbl WHERE s_name = 't' AND s_address_t = 'a'"
