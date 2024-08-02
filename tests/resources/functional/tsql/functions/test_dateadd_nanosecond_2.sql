-- ## DATEADD with the NANOSECOND keyword
--
-- Databricks SQl does not directly support `DATEADD`, so it is translated to the equivalent
-- INTERVAL increment NS

-- tsql sql:
SELECT DATEADD(NS, 7, col1) AS add_minutes_col1 FROM tabl;

-- databricks sql:
SELECT col1 + INTERVAL 7 NANOSECOND AS add_minutes_col1 FROM tabl;
