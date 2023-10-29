-- see https://docs.snowflake.com/en/sql-reference/functions/try_base64_decode_string

SELECT TRY_BASE64_DECODE_STRING(BASE64_ENCODE('HELLO'));