-- see https://docs.snowflake.com/en/sql-reference/functions/bitand_agg

select s2, bitand_agg(k), bitand_agg(d) from bitwise_example group by s2
    order by 3;