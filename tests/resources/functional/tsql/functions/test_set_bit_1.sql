-- ## SET_BIT
--
-- The SET_BIT function is identical in TSql and Databricks, save for a renaming of the function.
--
-- tsql sql:
SELECT SET_BIT(42, 7);

-- databricks sql:
SELECT SETBIT(42, 7);
