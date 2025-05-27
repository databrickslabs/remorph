from databricks.labs.remorph.reconcile.dialects.utils import get_dialect
from databricks.labs.remorph.reconcile.query_builder.count_query import CountQueryBuilder
from databricks.labs.remorph.reconcile.recon_config import Layer


def test_count_query(table_mapping_with_opts):
    source_query = CountQueryBuilder(
        mapping=table_mapping_with_opts, layer=Layer.SOURCE, dialect=get_dialect("oracle")
    ).build_query()
    target_query = CountQueryBuilder(
        mapping=table_mapping_with_opts, layer=Layer.TARGET, dialect=get_dialect("databricks")
    ).build_query()
    assert source_query == "SELECT COUNT(1) AS count FROM :tbl WHERE s_name = 't' AND s_address = 'a'"
    assert target_query == "SELECT COUNT(1) AS count FROM :tbl WHERE s_name = 't' AND s_address_t = 'a'"
