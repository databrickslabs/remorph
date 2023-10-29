-- see https://docs.snowflake.com/en/sql-reference/functions/try_hex_decode_string

CREATE TABLE hex (v VARCHAR, hex_string VARCHAR, garbage VARCHAR);
INSERT INTO hex (v, hex_string, garbage) 
  SELECT 'AaBb', HEX_ENCODE('AaBb'), '127';