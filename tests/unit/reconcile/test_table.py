from databricks.labs.lakebridge.reconcile.recon_config import Filters


def test_table_column_mapping(table_mapping_factory):
    mapping = table_mapping_factory(
        join_columns=["s_suppkey", "s_nationkey"],
        filters=Filters(source="s_nationkey=1"),
    )

    assert mapping.to_src_col_map is None
    assert mapping.to_src_col_map is None


def test_table_select_columns(table_mapping_factory, table_schema):
    schema, _ = table_schema
    mapping = table_mapping_factory(
        select_columns=["s_nationkey", "s_suppkey"],
    )

    assert mapping.get_select_columns(schema, "source") == {"s_nationkey", "s_suppkey"}
    assert len(mapping.get_select_columns(schema, "source")) == 2
