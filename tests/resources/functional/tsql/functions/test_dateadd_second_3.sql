-- DATEADD with the S keyword
--
-- Databricks SQl does not directly support `DATEADD`, so it is translated to the equivalent
-- INTERVAL increment SECOND

-- tsql sql:
SELECT DATEADD(s, 7, col1) AS add_minutes_col1 FROM tabl;

-- databricks sql:
SELECT (col1 + INTERVAL 7 SECOND) AS add_minutes_col1 FROM tabl;
