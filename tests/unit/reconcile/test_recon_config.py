from databricks.labs.remorph.reconcile.recon_config import (
    ColumnMapping,
    Transformation,
    TransformRuleMapping,
)
from tests.unit.reconcile.query_builder.test_conf import TestConf


def test_table_without_join_column():
    table_conf = TestConf().get_table_conf_default

    assert table_conf.list_to_dict(Transformation, "column_name") == {}
    assert table_conf.list_to_dict(ColumnMapping, "source_name") == {}
    assert table_conf.get_join_columns == set()
    assert table_conf.get_drop_columns == set()
    assert table_conf.get_partition_column("source") == set()
    assert table_conf.get_partition_column("target") == set()
    assert table_conf.get_filter("source") == " 1 = 1 "
    assert table_conf.get_filter("target") == " 1 = 1 "
    assert table_conf.get_threshold_columns == set()


def test_table_with_all_options():
    table_conf = TestConf().get_table_conf_all_options

    assert table_conf.list_to_dict(Transformation, "column_name") == {
        "s_address": Transformation(column_name="s_address", source="trim(s_address)", target="trim(s_address_t)"),
        "s_phone": Transformation(column_name="s_phone", source="trim(s_phone)", target="trim(s_phone)"),
        "s_name": Transformation(column_name="s_name", source="trim(s_name)", target="trim(s_name)"),
    }
    assert table_conf.list_to_dict(ColumnMapping, "source_name") == {
        "s_suppkey": ColumnMapping(source_name="s_suppkey", target_name="s_suppkey_t"),
        "s_address": ColumnMapping(source_name="s_address", target_name="s_address_t"),
    }
    assert table_conf.get_join_columns == {"s_suppkey"}
    assert table_conf.get_drop_columns == {"s_comment"}
    assert table_conf.get_partition_column("source") == {"s_nationkey"}
    assert table_conf.get_partition_column("target") == set()
    assert table_conf.get_filter("source") == "s_name='t' and s_address='a'"
    assert table_conf.get_filter("target") == "s_name='t' and s_address_t='a'"
    assert table_conf.get_threshold_columns == {"s_acctbal"}


def test_get_column_expr_without_alias():
    tfrm = TransformRuleMapping(column_name="s_address", transformation="trim(s_address)", alias_name="s_address_t")
    assert tfrm.get_column_expr_without_alias() == "trim(s_address)"

    tfrm = TransformRuleMapping(column_name="s_address", transformation=None, alias_name="s_address")
    assert tfrm.get_column_expr_without_alias() == "s_address"


def test_get_column_expr_with_alias():
    tfrm = TransformRuleMapping(column_name="s_phone", transformation="trim(s_phone)", alias_name="s_phone_t")
    assert tfrm.get_column_expr_with_alias() == "trim(s_phone) as s_phone_t"
