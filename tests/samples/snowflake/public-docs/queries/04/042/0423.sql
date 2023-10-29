-- see https://docs.snowflake.com/en/sql-reference/functions/try_base64_decode_string

CREATE TABLE base64 (v VARCHAR, base64_string VARCHAR, garbage VARCHAR);
INSERT INTO base64 (v, base64_string, garbage) 
  SELECT 'HELLO', BASE64_ENCODE('HELLO'), '127';