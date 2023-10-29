-- see https://docs.snowflake.com/en/sql-reference/functions/base64_decode_binary

SET MY_STRING = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()abcdefghijklmnopqrstuvwzyz1234567890[]{};:,./<>?-=~';
CREATE OR REPLACE TABLE binary_table (v VARCHAR, b BINARY, b64_string VARCHAR);
INSERT INTO binary_table (v) VALUES ($MY_STRING);
UPDATE binary_table SET b = TO_BINARY(v, 'UTF-8');
UPDATE binary_table SET b64_string = BASE64_ENCODE(b, 0, '$');