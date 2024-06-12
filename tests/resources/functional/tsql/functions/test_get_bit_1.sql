-- ## GET_BIT
--
-- The GET_BIT function is identical in TSql and Databricks.
--
-- tsql sql:
SELECT GET_BIT(42, 7);

-- databricks sql:
SELECT BIT_COUNT(42);
