-- see https://docs.snowflake.com/en/sql-reference/functions/boolxor

SELECT BOOLXOR(2, 0), BOOLXOR(1, -1), BOOLXOR(0, 0), BOOLXOR(NULL, 3), BOOLXOR(NULL, 0), BOOLXOR(NULL, NULL);
