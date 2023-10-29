-- see https://docs.snowflake.com/en/sql-reference/functions/parse_json

select n, v, typeof(v)
    from vartab
    order by n;