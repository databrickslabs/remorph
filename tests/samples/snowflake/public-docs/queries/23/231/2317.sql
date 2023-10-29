-- see https://docs.snowflake.com/en/sql-reference/functions/regexp_instr

select regexp_instr('It was the best of times, it was the worst of times', '\\bwas\\b', 1, 1) as "result" from dual;
