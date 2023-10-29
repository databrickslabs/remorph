-- see https://docs.snowflake.com/en/sql-reference/functions/bitxor_agg

select bitxor_agg(k), bitxor_agg(d), bitxor_agg(s1) from bitwise_example;