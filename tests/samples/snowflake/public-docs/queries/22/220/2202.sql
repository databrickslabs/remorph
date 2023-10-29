-- see https://docs.snowflake.com/en/sql-reference/functions/bitor_agg

select bitor_agg(s2) from bitwise_example;