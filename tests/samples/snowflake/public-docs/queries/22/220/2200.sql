-- see https://docs.snowflake.com/en/sql-reference/functions/bitand_agg

select bitand_agg(s2) from bitwise_example;