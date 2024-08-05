-- ## SET_BIT
--
-- The SET_BIT function is identical in TSql and Databricks, save for a renaming of the function.
--
-- tsql sql:
SELECT SET_BIT(42, 7, 0);

-- databricks sql:
SELECT 42 & -1 ^ SHIFTLEFT(1, 7) | SHIFTRIGHT(0, 7);
