-- see https://docs.snowflake.com/en/sql-reference/functions/bitand_agg

select bitand_agg(k), bitand_agg(d), bitand_agg(s1) from bitwise_example;