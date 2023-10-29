-- see https://docs.snowflake.com/en/sql-reference/functions/regexp_replace

select regexp_replace('It was the best of times, it was the worst of times', '( ){1,}','') as "result" from dual;
