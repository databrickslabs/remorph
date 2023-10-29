-- see https://docs.snowflake.com/en/sql-reference/functions/bitor_agg

select bitor_agg(k), bitor_agg(d), bitor_agg(s1) from bitwise_example;