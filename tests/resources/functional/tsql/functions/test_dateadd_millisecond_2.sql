-- DATEADD with the MS keyword
--
-- Databricks SQl does not directly support `DATEADD`, so it is translated to the equivalent
-- INTERVAL increment MILLISECOND

-- tsql sql:
SELECT DATEADD(ms, 7, col1) AS add_milliseconds_col1 FROM tabl;

-- databricks sql:
SELECT (col1 + INTERVAL 7 MILLISECOND) AS add_milliseconds_col1 FROM tabl;
