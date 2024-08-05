-- ## SET_BIT
--
-- The SET_BIT function is identical in TSql and Databricks, save for a renaming of the function.
--
-- tsql sql:
SELECT SET_BIT(42, 7, 0);

-- databricks sql:
SELECT BIT_OR(BIT_AND(42, BIT_XOR(-1, SHIFT_LEFT(1, 7))), SHIFT_RIGHT(0, 7));
