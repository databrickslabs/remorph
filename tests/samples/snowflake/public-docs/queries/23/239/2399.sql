-- see https://docs.snowflake.com/en/sql-reference/functions-regexp

select w2
    from wildcards
    where regexp_like(w2, '\\' || '?');