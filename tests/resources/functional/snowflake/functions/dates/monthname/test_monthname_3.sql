-- snowflake sql:
SELECT MONTHNAME(TO_DATE('2020-01-01')) AS MONTH;

-- databricks sql:
SELECT DATE_FORMAT(cast('2020-01-01' as DATE), 'MMM') AS MONTH;
