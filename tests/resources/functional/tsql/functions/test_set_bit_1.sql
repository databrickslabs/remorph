-- ## SET_BIT
--
-- The SET_BIT function does not exist in Databricks SQL, so we must use bit functions
--
-- tsql sql:
SELECT SET_BIT(42, 7);

-- databricks sql:
SELECT BIT_OR(42, SHIFT_LEFT(1, 7));
