-- see https://docs.snowflake.com/en/sql-reference/functions/to_binary

SELECT v, HEX_DECODE_STRING(TO_VARCHAR(b, 'HEX')) FROM binary_test;