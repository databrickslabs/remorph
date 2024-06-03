-- DATEADD with the WW keyword
--
-- Databricks SQl does not directly support `DATEADD`, so it is translated to the equivalent
-- DATE_ADD with the number of weeks multiplied by 7.

-- tsql sql:
SELECT DATEADD(ww, 2, col1) AS add_weeks_col1 FROM tabl;

-- databricks sql:
SELECT DATE_ADD(col1, 2*7) AS add_weeks_col1 FROM tabl;
