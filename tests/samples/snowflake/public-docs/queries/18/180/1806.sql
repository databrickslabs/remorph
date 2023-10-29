-- see https://docs.snowflake.com/en/sql-reference/functions/try_hex_decode_string

SELECT v, hex_string, TRY_HEX_DECODE_STRING(hex_string), TRY_HEX_DECODE_STRING(garbage) FROM hex;