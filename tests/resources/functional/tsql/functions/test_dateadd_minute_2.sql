-- ## DATEADD with the MI keyword
--
-- Databricks SQl does not directly support `DATEADD`, so it is translated to the equivalent
-- INTERVAL increment MINUTE

-- tsql sql:
SELECT DATEADD(mi, 7, col1) AS add_minutes_col1 FROM tabl;

-- databricks sql:
SELECT (col1 + INTERVAL 7 MINUTE) AS add_minutes_col1 FROM tabl;
