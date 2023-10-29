-- see https://docs.snowflake.com/en/sql-reference/functions/length

CREATE TABLE binary_table (v VARCHAR, 
  b_hex BINARY, b_base64 BINARY, b_utf8 BINARY);
INSERT INTO binary_table (v) VALUES ('hello');
UPDATE binary_table SET 
  b_hex    = TO_BINARY(HEX_ENCODE(v), 'HEX'),
  b_base64 = TO_BINARY(BASE64_ENCODE(v), 'BASE64'),
  b_utf8   = TO_BINARY(v, 'UTF-8')
  ;