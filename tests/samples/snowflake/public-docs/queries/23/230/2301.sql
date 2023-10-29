-- see https://docs.snowflake.com/en/sql-reference/functions/as

select n, as_real(v), typeof(v)
    from vartab
    order by n;