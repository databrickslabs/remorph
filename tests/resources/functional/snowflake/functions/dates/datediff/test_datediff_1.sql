-- snowflake sql:
SELECT datediff(yrs, TIMESTAMP'2021-02-28 12:00:00', TIMESTAMP'2021-03-28 12:00:00');

-- databricks sql:
SELECT
  DATEDIFF(
    year,
    CAST('2021-02-28 12:00:00' AS TIMESTAMP),
    CAST('2021-03-28 12:00:00' AS TIMESTAMP)
  );
