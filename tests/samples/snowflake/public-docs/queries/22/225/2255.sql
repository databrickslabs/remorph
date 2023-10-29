-- see https://docs.snowflake.com/en/sql-reference/functions/regexp_substr

select id, regexp_substr(string1, 'the\\W+(\\w+)', 1, 2, 'e', 1) as "RESULT"
    from demo2
    order by id;