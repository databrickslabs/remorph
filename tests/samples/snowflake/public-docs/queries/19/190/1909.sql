-- see https://docs.snowflake.com/en/sql-reference/functions/to_binary

UPDATE binary_test SET b = TO_BINARY(HEX_ENCODE(v), 'HEX');