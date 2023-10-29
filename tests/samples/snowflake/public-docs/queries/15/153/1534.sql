-- see https://docs.snowflake.com/en/sql-reference/functions/nvl2

SELECT a, b, c, NVL2(a, b, c) FROM i2;
