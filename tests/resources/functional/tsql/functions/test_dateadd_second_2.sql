-- ## DATEADD with the SS keyword
--
-- Databricks SQl does not directly support `DATEADD`, so it is translated to the equivalent
-- INTERVAL increment SECOND

-- tsql sql:
SELECT DATEADD(ss, 7, col1) AS add_seconds_col1 FROM tabl;

-- databricks sql:
SELECT (col1 + INTERVAL 7 SECOND) AS add_seconds_col1 FROM tabl;
