-- see https://docs.snowflake.com/en/sql-reference/functions/get_query_operator_stats

select x1.i, x2.i
    from x1 inner join x2 on x2.i = x1.i
    order by x1.i, x2.i;