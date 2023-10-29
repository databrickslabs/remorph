-- see https://docs.snowflake.com/en/sql-reference/functions/hex_decode_binary

SELECT v, b, HEX_DECODE_STRING(TO_VARCHAR(b)) FROM binary_table;