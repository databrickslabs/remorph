-- see https://docs.snowflake.com/en/sql-reference/functions/dateadd

SELECT DATEADD(MONTH, 1, '2000-01-31'::DATE) AS DIFFERENT_DAY;