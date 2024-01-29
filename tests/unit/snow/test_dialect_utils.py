from databricks.labs.remorph.snow.dialect_utils import check_for_unsupported_lca


def test_snow_query_with_no_unsupported_lca_usage():
    dialect = "SNOWFLAKE"
    sql = """
        SELECT
            t.col1,
            t.col2,
            t.col3 AS ca,
        FROM table1 t
    """
    filename = "test_file1.sql"

    error_list = check_for_unsupported_lca(dialect, sql, filename)
    assert not error_list


def test_snow_query_with_lca_in_where():
    dialect = "SNOWFLAKE"
    sql = """
        SELECT
            t.col1,
            t.col2,
            t.col3 AS ca,
        FROM table1 t
        WHERE ca in ('v1', 'v2')
    """
    filename = "test_file2.sql"

    error_list = check_for_unsupported_lca(dialect, sql, filename)
    assert error_list


def test_snow_query_with_lca_in_window():
    dialect = "SNOWFLAKE"
    sql = """
        SELECT
            t.col1,
            t.col2,
            t.col3 AS ca,
            ROW_NUMBER() OVER (PARTITION by ca ORDER BY t.col2 DESC) AS rn
        FROM table1 t
    """
    filename = "test_file3.sql"

    error_list = check_for_unsupported_lca(dialect, sql, filename)
    assert error_list


def test_snow_query_with_error():
    dialect = "SNOWFLAKE"
    sql = """
        SELECT
            t.col1
            t.col2,
            t.col3 AS ca,
        FROM table1 t
    """
    filename = "test_file4.sql"

    error_list = check_for_unsupported_lca(dialect, sql, filename)
    assert error_list
