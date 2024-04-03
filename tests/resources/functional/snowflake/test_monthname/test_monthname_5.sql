
-- source:
SELECT d, MONTHNAME(d) FROM dates;

-- databricks_sql:
SELECT d, DATE_FORMAT(d, 'MMM') FROM dates;
