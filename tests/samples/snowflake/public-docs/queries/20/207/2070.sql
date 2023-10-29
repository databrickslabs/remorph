-- see https://docs.snowflake.com/en/sql-reference/functions/get_query_operator_stats

select *
    from table(get_query_operator_stats(last_query_id()));