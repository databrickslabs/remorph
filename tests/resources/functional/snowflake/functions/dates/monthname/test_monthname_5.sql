-- snowflake sql:
SELECT d, MONTHNAME(d) FROM dates;

-- databricks sql:
SELECT d, DATE_FORMAT(d, 'MMM') FROM dates;
