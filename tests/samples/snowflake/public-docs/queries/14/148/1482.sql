-- see https://docs.snowflake.com/en/sql-reference/functions/timeadd

SELECT TO_DATE('2013-05-08') AS v1, DATEADD(year, 2, TO_DATE('2013-05-08')) AS v;