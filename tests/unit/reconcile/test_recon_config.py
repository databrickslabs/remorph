def test_table_without_join_column(table_mapping_factory):
    mapping = table_mapping_factory()
    assert mapping.get_join_columns("source") is None
    assert mapping.get_drop_columns("source") == set()
    assert mapping.get_partition_column("source") == set()
    assert mapping.get_partition_column("target") == set()
    assert mapping.get_filter("source") is None
    assert mapping.get_filter("target") is None
    assert mapping.get_threshold_columns("source") == set()


def test_table_with_all_options(table_mapping_with_opts):
    ## layer == source

    assert table_mapping_with_opts.get_join_columns("source") == {"s_nationkey", "s_suppkey"}
    assert table_mapping_with_opts.get_drop_columns("source") == {"s_comment"}
    assert table_mapping_with_opts.get_partition_column("source") == {"s_nationkey"}
    assert table_mapping_with_opts.get_partition_column("target") == set()
    assert table_mapping_with_opts.get_filter("source") == "s_name='t' and s_address='a'"
    assert table_mapping_with_opts.get_threshold_columns("source") == {"s_acctbal"}

    ## layer == target
    assert table_mapping_with_opts.get_join_columns("target") == {"s_nationkey_t", "s_suppkey_t"}
    assert table_mapping_with_opts.get_drop_columns("target") == {"s_comment_t"}
    assert table_mapping_with_opts.get_partition_column("target") == set()
    assert table_mapping_with_opts.get_filter("target") == "s_name='t' and s_address_t='a'"
    assert table_mapping_with_opts.get_threshold_columns("target") == {"s_acctbal_t"}


def test_table_without_column_mapping(table_mapping_factory, column_mapping):
    mapping = table_mapping_factory()

    assert mapping.get_tgt_to_src_col_mapping_list(["s_address", "s_name"]) == {"s_address", "s_name"}
    assert mapping.get_layer_tgt_to_src_col_mapping("s_address_t", "target") == "s_address_t"
    assert mapping.get_layer_tgt_to_src_col_mapping("s_address", "source") == "s_address"
    assert mapping.get_src_to_tgt_col_mapping_list(["s_address", "s_name"], "source") == {"s_address", "s_name"}
    assert mapping.get_src_to_tgt_col_mapping_list(["s_address", "s_name"], "target") == {"s_address", "s_name"}
    assert mapping.get_layer_src_to_tgt_col_mapping("s_address", "source") == "s_address"
