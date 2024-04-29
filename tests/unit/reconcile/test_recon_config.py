def test_table_without_join_column(table_conf_mock):
    table_conf = table_conf_mock()
    assert table_conf.get_join_columns("source") == set()
    assert table_conf.get_drop_columns("source") == set()
    assert table_conf.get_partition_column("source") == set()
    assert table_conf.get_partition_column("target") == set()
    assert table_conf.get_filter("source") is None
    assert table_conf.get_filter("target") is None
    assert table_conf.get_threshold_columns("source") == set()


def test_table_with_all_options(table_conf_with_opts):
    ## layer == source

    assert table_conf_with_opts.get_join_columns("source") == {"s_nationkey", "s_suppkey"}
    assert table_conf_with_opts.get_drop_columns("source") == {"s_comment"}
    assert table_conf_with_opts.get_partition_column("source") == {"s_nationkey"}
    assert table_conf_with_opts.get_partition_column("target") == set()
    assert table_conf_with_opts.get_filter("source") == "s_name='t' and s_address='a'"
    assert table_conf_with_opts.get_threshold_columns("source") == {"s_acctbal"}

    ## layer == target
    assert table_conf_with_opts.get_join_columns("target") == {"s_nationkey_t", "s_suppkey_t"}
    assert table_conf_with_opts.get_drop_columns("target") == {"s_comment_t"}
    assert table_conf_with_opts.get_partition_column("target") == set()
    assert table_conf_with_opts.get_filter("target") == "s_name='t' and s_address_t='a'"
    assert table_conf_with_opts.get_threshold_columns("target") == {"s_acctbal_t"}
