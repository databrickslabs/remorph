-- see https://docs.snowflake.com/en/sql-reference/functions/regexp_count

select regexp_count('It was the best of times, it was the worst of times', '\\bwas\\b', 1) as "result" from dual;
