
-- snowflake sql:
SELECT MONTHNAME(TO_DATE('2015-05-01')) AS MONTH;

-- databricks sql:
SELECT DATE_FORMAT(cast('2015-05-01' as date), 'MMM') AS MONTH;
