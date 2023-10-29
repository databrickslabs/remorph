-- see https://docs.snowflake.com/en/sql-reference/functions/typeof

select n, v, typeof(v)
    from vartab
    order by n;