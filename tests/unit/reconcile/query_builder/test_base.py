from databricks.labs.remorph.reconcile.query_builder.base import QueryBuilder
from databricks.labs.remorph.reconcile.recon_config import ColumnMapping, Transformation
from tests.unit.reconcile.query_builder.test_conf import TestConf


def test_base_querybuilder_with_defaults():
    table_conf = TestConf().get_table_conf_default
    schema = TestConf().get_schema
    query_builder = QueryBuilder(table_conf, schema, "source", "oracle")

    assert query_builder.source == "oracle"
    assert query_builder.layer == "source"
    assert query_builder.table_conf == table_conf
    assert query_builder.schema_dict == {v.column_name: v for v in schema}
    assert query_builder.tgt_col_mapping == {}
    assert query_builder.src_col_mapping == {}
    assert query_builder.transform_dict == {}
    assert query_builder.select_columns == {v.column_name for v in schema}
    assert query_builder.table_name == "{schema_name}.supplier"


def test_base_querybuilder_with_all_options():
    table_conf = TestConf().get_table_conf_all_options
    alias_schema = TestConf().get_alias_schema
    query_builder = QueryBuilder(table_conf, alias_schema, "target", "snowflake")

    assert query_builder.source == "snowflake"
    assert query_builder.layer == "target"
    assert query_builder.table_conf == table_conf
    assert query_builder.schema_dict == {v.column_name: v for v in alias_schema}
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
