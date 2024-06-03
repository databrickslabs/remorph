-- DATEADD with the M keyword
--
-- Databricks SQl does not directly support DATEADD, so it is translated to the equivalent
-- ADD_MONTHS function.


-- tsql sql:
SELECT DATEADD(m, 1, col1) AS add_months_col1 FROM tabl;

-- databricks sql:
SELECT ADD_MONTHS(col1, 1) AS add_months_col1 FROM tabl;
