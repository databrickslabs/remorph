-- see https://docs.snowflake.com/en/sql-reference/functions/dateadd

SELECT DATEADD(MONTH, 1, '2000-02-29'::DATE) AS RESULT;