-- see https://docs.snowflake.com/en/sql-reference/functions/hex_decode_binary

CREATE TABLE binary_table (v VARCHAR, b BINARY);
INSERT INTO binary_table (v, b) 
    SELECT 'HELLO', HEX_DECODE_BINARY(HEX_ENCODE('HELLO'));