-- snowflake sql:
SELECT DAYNAME('2015-04-03 10:00') AS MONTH;

-- databricks sql:
SELECT DATE_FORMAT('2015-04-03 10:00', 'E') AS MONTH;
