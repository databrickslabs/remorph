-- see https://docs.snowflake.com/en/sql-reference/functions/try_base64_decode_string

SELECT v, base64_string, TRY_BASE64_DECODE_STRING(base64_string), TRY_BASE64_DECODE_STRING(garbage) FROM base64;