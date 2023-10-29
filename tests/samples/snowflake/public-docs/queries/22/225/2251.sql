-- see https://docs.snowflake.com/en/sql-reference/functions/regexp_substr

select id, 
    regexp_substr(string1, 'A\\W+(\\w)(\\w)(\\w)', 1, 1, 'e', 1) as "RESULT1",
    regexp_substr(string1, 'A\\W+(\\w)(\\w)(\\w)', 1, 1, 'e', 2) as "RESULT2",
    regexp_substr(string1, 'A\\W+(\\w)(\\w)(\\w)', 1, 1, 'e', 3) as "RESULT3"
    from demo3;