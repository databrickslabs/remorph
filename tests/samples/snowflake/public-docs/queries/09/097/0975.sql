-- see https://docs.snowflake.com/en/sql-reference/functions/array_distinct

SELECT ARRAY_DISTINCT(['A', 'A', 'B', NULL, NULL]);
