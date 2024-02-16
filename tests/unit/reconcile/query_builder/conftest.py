def assert_query_config_dataclass(actual, expected):
    assert actual.hash_columns == actual.hash_columns
    assert actual.select_columns == expected.select_columns
    assert actual.hash_col_transformation == expected.hash_col_transformation
