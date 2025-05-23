from databricks.labs.remorph.reconcile.recon_config import Layer


def test_table_without_join_column(table_mapping_builder):
    table_mapping_builder = table_mapping_builder()
    assert table_conf.get_join_columns(Layer.SOURCE) is None
    assert table_conf.get_drop_columns(Layer.SOURCE) == set()
    assert table_conf.get_partition_column(Layer.SOURCE) == set()
    assert table_conf.get_partition_column(Layer.TARGET) == set()
    assert table_conf.get_filter(Layer.SOURCE) is None
    assert table_conf.get_filter(Layer.TARGET) is None
    assert table_conf.get_threshold_columns(Layer.SOURCE) == set()


def test_table_with_all_options(table_mapping_with_opts):
    ## layer == source

    assert table_mapping_with_opts.get_join_columns(Layer.SOURCE) == {"s_nationkey", "s_suppkey"}
    assert table_mapping_with_opts.get_drop_columns(Layer.SOURCE) == {"s_comment"}
    assert table_mapping_with_opts.get_partition_column(Layer.SOURCE) == {"s_nationkey"}
    assert table_mapping_with_opts.get_partition_column(Layer.TARGET) == set()
    assert table_mapping_with_opts.get_filter(Layer.SOURCE) == "s_name='t' and s_address='a'"
    assert table_mapping_with_opts.get_threshold_columns(Layer.SOURCE) == {"s_acctbal"}

    ## layer == target
    assert table_mapping_with_opts.get_join_columns("target") == {"s_nationkey_t", "s_suppkey_t"}
    assert table_mapping_with_opts.get_drop_columns("target") == {"s_comment_t"}
    assert table_mapping_with_opts.get_partition_column(Layer.TARGET) == set()
    assert table_mapping_with_opts.get_filter(Layer.TARGET) == "s_name='t' and s_address_t='a'"
    assert table_mapping_with_opts.get_threshold_columns("target") == {"s_acctbal_t"}


def test_table_without_column_mapping(table_mapping_builder, column_mapping):
    table_mapping_builder = table_mapping_builder()

    assert table_conf.get_tgt_to_src_col_mapping_list(["s_address", "s_name"]) == {"s_address", "s_name"}
    assert table_conf.get_layer_tgt_to_src_col_mapping("s_address_t", "target") == "s_address_t"
    assert table_conf.get_layer_tgt_to_src_col_mapping("s_address", "source") == "s_address"
    assert table_conf.get_src_to_tgt_col_mapping_list(["s_address", "s_name"], "source") == {"s_address", "s_name"}
    assert table_conf.get_src_to_tgt_col_mapping_list(["s_address", "s_name"], "target") == {"s_address", "s_name"}
    assert table_conf.get_layer_src_to_tgt_col_mapping("s_address", "source") == "s_address"
