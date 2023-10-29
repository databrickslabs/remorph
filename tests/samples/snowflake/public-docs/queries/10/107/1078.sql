-- see https://docs.snowflake.com/en/sql-reference/functions/generator

SELECT COUNT(seq4()) FROM TABLE(GENERATOR(TIMELIMIT => 10)) v;
