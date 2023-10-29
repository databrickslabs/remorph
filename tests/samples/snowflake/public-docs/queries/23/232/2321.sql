-- see https://docs.snowflake.com/en/sql-reference/functions/regexp_replace

select regexp_replace('It was the best of times, it was the worst of times', 'times','days',1,2) as "result" from dual;
