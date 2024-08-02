-- ## DATEADD with the MILLISECOND keyword
--
-- Databricks SQl does not directly support `DATEADD`, so it is translated to the equivalent
-- INTERVAL increment MILLISECOND

-- tsql sql:
SELECT DATEADD(millisecond, 7, col1) AS add_minutes_col1 FROM tabl;

-- databricks sql:
SELECT col1 + INTERVAL 7 MILLISECOND AS add_minutes_col1 FROM tabl;
