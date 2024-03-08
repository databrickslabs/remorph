from databricks.labs.remorph.snow.dialect_utils import check_for_unsupported_lca


def test_query_with_no_unsupported_lca_usage():
    dialect = "SNOWFLAKE"
    sql = """
        SELECT
            t.col1,
            t.col2,
            t.col3 AS ca,
        FROM table1 t
    """
    filename = "test_file1.sql"

    error = check_for_unsupported_lca(dialect, sql, filename)
    assert not error


def test_query_with_valid_alias_usage():
    dialect = "SNOWFLAKE"
    sql = """
        WITH web_v1 as (
        select
          ws_item_sk item_sk, d_date,
          sum(sum(ws_sales_price))
              over (partition by ws_item_sk order by d_date rows between unbounded preceding and current row) cume_sales
        from web_sales
            ,date_dim
        where ws_sold_date_sk=d_date_sk
          and d_month_seq between 1212 and 1212+11
          and ws_item_sk is not NULL
        group by ws_item_sk, d_date),
        store_v1 as (
        select
          ss_item_sk item_sk, d_date,
          sum(sum(ss_sales_price))
              over (
                partition by ss_item_sk order by d_date rows between unbounded preceding and current row
              ) cume_sales
        from store_sales
            ,date_dim
        where ss_sold_date_sk=d_date_sk
          and d_month_seq between 1212 and 1212+11
          and ss_item_sk is not NULL
        group by ss_item_sk, d_date)
         select  *
        from (select item_sk
             ,d_date
             ,web_sales
             ,store_sales
             ,max(web_sales)
                 over (
                    partition by item_sk order by d_date rows between unbounded preceding and current row
                 ) web_cumulative
             ,max(store_sales)
                 over (
                    partition by item_sk order by d_date rows between unbounded preceding and current row
                 ) store_cumulative
             from (select case when web.item_sk is not null then web.item_sk else store.item_sk end item_sk
                         ,case when web.d_date is not null then web.d_date else store.d_date end d_date
                         ,web.cume_sales web_sales
                         ,store.cume_sales store_sales
                   from web_v1 web full outer join store_v1 store on (web.item_sk = store.item_sk
                                                                  and web.d_date = store.d_date)
                  )x )y
        where web_cumulative > store_cumulative
        order by item_sk
                ,d_date
        limit 100;
    """
    filename = "test_file1.sql"

    error = check_for_unsupported_lca(dialect, sql, filename)
    assert not error


def test_query_with_lca_in_where():
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

    error = check_for_unsupported_lca(dialect, sql, filename)
    assert error


def test_query_with_lca_in_window():
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

    error = check_for_unsupported_lca(dialect, sql, filename)
    assert error


def test_query_with_error():
    dialect = "SNOWFLAKE"
    sql = """
        SELECT
            t.col1
            t.col2,
            t.col3 AS ca,
        FROM table1 t
    """
    filename = "test_file4.sql"

    error = check_for_unsupported_lca(dialect, sql, filename)
    assert not error


def test_query_with_same_alias_and_column_name():
    dialect = "SNOWFLAKE"
    sql = """
    select ca_zip
     from (
      SELECT 
      substr(ca_zip,1,5) ca_zip, 
      trim(name) as name,
      count(*) over( partition by ca_zip)
      FROM customer_address
      WHERE substr(ca_zip,1,5) IN ('89436', '30868'));
    """
    filename = "test_file5.sql"

    error = check_for_unsupported_lca(dialect, sql, filename)
    assert not error
