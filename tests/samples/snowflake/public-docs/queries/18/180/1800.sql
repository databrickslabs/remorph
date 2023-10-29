-- see https://docs.snowflake.com/en/sql-reference/functions/base64_decode_binary

SELECT v, b, b64_string, 
        BASE64_DECODE_BINARY(b64_string) AS FROM_BASE64_BACK_TO_BINARY,
        TO_VARCHAR(BASE64_DECODE_BINARY(b64_string), 'UTF-8') AS BACK_TO_STRING
    FROM binary_table;