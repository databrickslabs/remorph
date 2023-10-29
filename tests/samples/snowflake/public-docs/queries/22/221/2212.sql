-- see https://docs.snowflake.com/en/sql-reference/functions/booland_agg

select booland_agg('invalid type');

100037 (22018): Boolean value 'invalid_type' is not recognized