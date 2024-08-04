-- ## DATEADD with the MINUTE keyword
--
-- Databricks SQl does not directly support `DATEADD`, so it is translated to the equivalent
-- INTERVAL increment MINUTE

-- tsql sql:
SELECT DATEADD(minute, 7, col1) AS add_minutes_col1 FROM tabl;

-- databricks sql:
SELECT col1 + INTERVAL 7 MINUTE AS add_minutes_col1 FROM tabl;
