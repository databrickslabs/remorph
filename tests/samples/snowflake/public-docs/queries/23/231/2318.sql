-- see https://docs.snowflake.com/en/sql-reference/functions/regexp_instr

select regexp_instr('It was the best of times, it was the worst of times', 'the\\W+(\\w+)',1,1,0) as "result" from dual;
