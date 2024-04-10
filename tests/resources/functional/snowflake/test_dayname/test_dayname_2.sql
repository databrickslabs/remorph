
-- snowflake sql:
SELECT DAYNAME(TO_DATE('2015-05-01')) AS MONTH;

-- databricks sql:
SELECT DATE_FORMAT(cast('2015-05-01' as date), 'E') AS MONTH;
