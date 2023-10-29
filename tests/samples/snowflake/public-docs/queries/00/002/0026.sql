-- see https://docs.snowflake.com/en/sql-reference/functions/base64_decode_binary

-- Note that the binary data in column b is displayed in hexadecimal
--   format to make it human-readable.
SELECT v, b, b64_string FROM binary_table;