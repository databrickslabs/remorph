
-- snowflake sql:
SELECT datediff(mons, DATE'2021-02-28', DATE'2021-03-28');

-- databricks sql:
SELECT DATEDIFF(month, CAST('2021-02-28' AS DATE), CAST('2021-03-28' AS DATE));
