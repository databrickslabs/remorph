-- see https://docs.snowflake.com/en/sql-reference/functions/bitxor_agg

select bitxor_agg(s2) from bitwise_example;