from databricks.labs.remorph.reconcile.recon_config import Layer


def test_table_without_join_column(table_mapping_builder):
    table_mapping = table_mapping_builder()
    assert table_mapping.get_join_columns(Layer.SOURCE) is None
    assert table_mapping.get_drop_columns(Layer.SOURCE) == set()
    assert table_mapping.get_partition_column(Layer.SOURCE) == set()
    assert table_mapping.get_partition_column(Layer.TARGET) == set()
    assert table_mapping.get_filter(Layer.SOURCE) is None
    assert table_mapping.get_filter(Layer.TARGET) is None
    assert table_mapping.get_threshold_columns(Layer.SOURCE) == set()


def test_table_with_all_options(table_mapping_with_opts):
    ## layer == source

    assert table_mapping_with_opts.get_join_columns(Layer.SOURCE) == {"s_nationkey", "s_suppkey"}
    assert table_mapping_with_opts.get_drop_columns(Layer.SOURCE) == {"s_comment"}
    assert table_mapping_with_opts.get_partition_column(Layer.SOURCE) == {"s_nationkey"}
    assert table_mapping_with_opts.get_partition_column(Layer.TARGET) == set()
    assert table_mapping_with_opts.get_filter(Layer.SOURCE) == "s_name='t' and s_address='a'"
    assert table_mapping_with_opts.get_threshold_columns(Layer.SOURCE) == {"s_acctbal"}

    ## layer == target
    assert table_mapping_with_opts.get_join_columns(Layer.TARGET) == {"s_nationkey_t", "s_suppkey_t"}
    assert table_mapping_with_opts.get_drop_columns(Layer.TARGET) == {"s_comment_t"}
    assert table_mapping_with_opts.get_partition_column(Layer.TARGET) == set()
    assert table_mapping_with_opts.get_filter(Layer.TARGET) == "s_name='t' and s_address_t='a'"
    assert table_mapping_with_opts.get_threshold_columns(Layer.TARGET) == {"s_acctbal_t"}


def test_table_without_column_mapping(table_mapping_builder, column_mappings):
    table_mapping = table_mapping_builder()

    assert table_mapping.get_tgt_to_src_col_mapping_list(["s_address", "s_name"]) == {"s_address", "s_name"}
    assert table_mapping.get_layer_tgt_to_src_col_mapping("s_address_t", Layer.TARGET) == "s_address_t"
    assert table_mapping.get_layer_tgt_to_src_col_mapping("s_address", Layer.SOURCE) == "s_address"
    assert table_mapping.get_src_to_tgt_col_mapping_list(["s_address", "s_name"], Layer.SOURCE) == {
        "s_address",
        "s_name",
    }
    assert table_mapping.get_src_to_tgt_col_mapping_list(["s_address", "s_name"], Layer.TARGET) == {
        "s_address",
        "s_name",
    }
    assert table_mapping.get_layer_src_to_tgt_col_mapping("s_address", Layer.SOURCE) == "s_address"
