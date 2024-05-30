-- DATEADD with the HH keyword
--
-- Databricks SQl does not directly support `DATEADD`, so it is translated to the equivalent
-- INTERVAL increment HOUR

-- tsql sql:
SELECT DATEADD(hh, 7, col1) AS add_hours_col1 FROM tabl;

-- databricks sql:
SELECT (col1 + INTERVAL 7 HOUR) AS add_hours_col1 FROM tabl;
