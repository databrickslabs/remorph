-- see https://docs.snowflake.com/en/sql-reference/functions/base64_decode_binary

SELECT v
    FROM binary_table;
SELECT b
    FROM binary_table;
SELECT b64_string
    FROM binary_table;
SELECT BASE64_DECODE_BINARY(b64_string, '$') AS FROM_BASE64_BACK_TO_BINARY
    FROM binary_table;
SELECT TO_VARCHAR(BASE64_DECODE_BINARY(b64_string, '$'), 'UTF-8') AS BACK_TO_STRING
    FROM binary_table;