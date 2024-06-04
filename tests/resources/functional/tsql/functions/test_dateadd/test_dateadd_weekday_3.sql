-- DATEADD with the W keyword
--
-- Databricks SQl does not directly support `DATEADD`, so it is translated to the equivalent
-- DATE_ADD as in the context of `DATEADD`, `day`, `dayofyear` and `weekday` are equivalent.

-- tsql sql:
SELECT DATEADD(W, 2, col1) AS add_days_col1 FROM tabl;

-- databricks sql:
SELECT DATE_ADD(col1, 2) AS add_days_col1 FROM tabl;
