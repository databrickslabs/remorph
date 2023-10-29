-- see https://docs.snowflake.com/en/sql-reference/functions/bit_length

SELECT v, b, BIT_LENGTH(v), BIT_LENGTH(b) FROM bl ORDER BY v;