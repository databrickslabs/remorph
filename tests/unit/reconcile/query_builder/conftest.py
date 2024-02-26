def assert_query_config_dataclass(actual, expected):
    assert actual.table_transform == expected.table_transform
