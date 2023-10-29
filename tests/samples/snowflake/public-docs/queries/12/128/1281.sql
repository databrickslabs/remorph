-- see https://docs.snowflake.com/en/sql-reference/functions/octet_length

SELECT OCTET_LENGTH('abc'), OCTET_LENGTH('\u0392'), OCTET_LENGTH(X'A1B2');
