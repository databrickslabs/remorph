-- see https://docs.snowflake.com/en/sql-reference/functions/hex_decode_string

SELECT v, b, HEX_DECODE_STRING(TO_VARCHAR(b)) FROM binary_table;