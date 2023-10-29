-- see https://docs.snowflake.com/en/sql-reference/functions/regexp

select v, v regexp 'San\\b.*' AS MATCHES
    from strings
    order by v;