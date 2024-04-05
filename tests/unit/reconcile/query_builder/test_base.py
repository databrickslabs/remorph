from databricks.labs.remorph.reconcile.query_builder.base import QueryBuilder
from databricks.labs.remorph.reconcile.recon_config import ColumnMapping, Transformation


def test_base_querybuilder_with_defaults(table_conf_mock, schema):
    table_conf = table_conf_mock()
    sch, _ = schema
    query_builder = QueryBuilder(table_conf, sch, "source", "oracle")

    assert query_builder.source == "oracle"
    assert query_builder.layer == "source"
    assert query_builder.table_conf == table_conf
    assert query_builder.schema_dict == {v.column_name: v for v in sch}
    assert query_builder.tgt_col_mapping == {}
    assert query_builder.src_col_mapping == {}
    assert query_builder.transform_dict == {}
    assert query_builder.select_columns == {v.column_name for v in sch}
    assert query_builder.table_name == "{schema_name}.supplier"


def test_base_querybuilder_with_all_options(table_conf_with_opts, schema):
    table_conf = table_conf_with_opts
    _, alias_sch = schema
    query_builder = QueryBuilder(table_conf, alias_sch, "target", "databricks")

    assert query_builder.source == "databricks"
    assert query_builder.layer == "target"
    assert query_builder.table_conf == table_conf
    assert query_builder.schema_dict == {v.column_name: v for v in alias_sch}
    assert query_builder.tgt_col_mapping == {
        "s_suppkey_t": ColumnMapping(source_name="s_suppkey", target_name="s_suppkey_t"),
        "s_address_t": ColumnMapping(source_name="s_address", target_name="s_address_t"),
    }
    assert query_builder.src_col_mapping == {
        "s_suppkey": ColumnMapping(source_name="s_suppkey", target_name="s_suppkey_t"),
        "s_address": ColumnMapping(source_name="s_address", target_name="s_address_t"),
    }
    assert query_builder.transform_dict == {
        "s_address": Transformation(column_name="s_address", source="trim(s_address)", target="trim(s_address_t)"),
        "s_phone": Transformation(column_name="s_phone", source="trim(s_phone)", target="trim(s_phone)"),
        "s_name": Transformation(column_name="s_name", source="trim(s_name)", target="trim(s_name)"),
    }
    assert query_builder.select_columns == {'s_suppkey', 's_address', 's_name'}
    assert query_builder.table_name == "{catalog_name}.{schema_name}.target_supplier"
