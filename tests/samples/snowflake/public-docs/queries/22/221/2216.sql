-- see https://docs.snowflake.com/en/sql-reference/functions/boolxor_agg

select boolxor_agg('invalid type');

100037 (22018): Boolean value 'invalid_type' is not recognized