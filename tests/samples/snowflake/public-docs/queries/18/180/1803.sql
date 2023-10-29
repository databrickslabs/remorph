-- see https://docs.snowflake.com/en/sql-reference/functions/base64_encode

SELECT v, base64_string, BASE64_DECODE_STRING(base64_string) 
    FROM base64_table;