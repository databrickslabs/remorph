-- ## DATEADD with the NANOSECOND keyword
--
-- Databricks SQl does not directly support `DATEADD`, so it is translated to the equivalent
-- INTERVAL increment NANOSECOND

-- tsql sql:
SELECT DATEADD(NANOSECOND, 7, col1) AS add_nanoseconds_col1 FROM tabl;

-- databricks sql:
SELECT (col1 + INTERVAL 7 NANOSECOND) AS add_nanoseconds_col1 FROM tabl;
