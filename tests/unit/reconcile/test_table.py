from databricks.labs.remorph.reconcile.recon_config import Filters


def test_table_column_mapping(table_mapping_builder):
    table_mapping = table_mapping_builder(
        join_columns=["s_suppkey", "s_nationkey"],
        filters=Filters(source="s_nationkey=1"),
    )

    assert table_mapping.to_src_col_map is None
    assert table_mapping.to_src_col_map is None


def test_table_select_columns(table_mapping_builder, table_schema):
    schema, _ = table_schema
    table_mapping = table_mapping_builder(
        select_columns=["s_nationkey", "s_suppkey"],
    )

    assert table_mapping.get_select_columns(schema, "source") == {"s_nationkey", "s_suppkey"}
    assert len(table_mapping.get_select_columns(schema, "source")) == 2
