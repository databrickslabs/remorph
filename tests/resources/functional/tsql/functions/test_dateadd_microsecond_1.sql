-- ## DATEADD with the MICROSECOND keyword
--
-- Databricks SQL does not directly support `DATEADD`, so it is translated to the equivalent
-- INTERVAL increment MICROSECOND

-- tsql sql:
SELECT DATEADD(MICROSECOND, 7, col1) AS add_microsecond_col1 FROM tabl;

-- databricks sql:
SELECT col1 + INTERVAL 7 MICROSECOND AS add_microsecond_col1 FROM tabl;
