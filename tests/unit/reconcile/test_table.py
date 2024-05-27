from databricks.labs.remorph.reconcile.recon_config import Filters


def test_table_column_mapping(table_conf_mock):
    table_conf = table_conf_mock(
        join_columns=["s_suppkey", "s_nationkey"],
        filters=Filters(source="s_nationkey=1"),
    )

    assert table_conf.to_src_col_map is None
    assert table_conf.to_src_col_map is None


def test_table_select_columns(table_conf_mock, table_schema):
    schema, _ = table_schema
    table_conf = table_conf_mock(
        select_columns=["s_nationkey", "s_suppkey"],
    )

    assert table_conf.get_select_columns(schema, "source") == {"s_nationkey", "s_suppkey"}
    assert len(table_conf.get_select_columns(schema, "source")) == 2
