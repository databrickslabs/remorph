-- see https://docs.snowflake.com/en/sql-reference/functions/regexp

select v, v regexp $$.*\s\\.*$$ AS MATCHES
    from strings
    order by v;