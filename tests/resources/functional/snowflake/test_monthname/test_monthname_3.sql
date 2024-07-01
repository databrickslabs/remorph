
-- IGNORED snowflake sql:
SELECT MONTH_NAME(TO_DATE('2020-01-01')) AS MONTH;

-- databricks sql:
SELECT DATE_FORMAT(cast('2020-01-01' as date), 'MMM') AS MONTH;
