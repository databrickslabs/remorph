-- see https://docs.snowflake.com/en/sql-reference/functions/hex_decode_binary

SELECT HEX_DECODE_BINARY(HEX_ENCODE(MD5_BINARY('Snowflake')));
