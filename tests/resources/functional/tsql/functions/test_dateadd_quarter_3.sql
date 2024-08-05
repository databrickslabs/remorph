-- ## DATEADD with the Q keyword
--
-- Databricks SQl does not directly support DATEADD, so it is translated to the equivalent
-- ADD_MONTHS function with the number of months multiplied by 3.

-- tsql sql:
SELECT DATEADD(q, 2, col1) AS add_quarters_col1 FROM tabl;

-- databricks sql:
SELECT ADD_MONTHS(col1, 2 * 3) AS add_quarters_col1 FROM tabl;
