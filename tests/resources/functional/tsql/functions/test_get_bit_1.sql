-- ## GET_BIT
--
-- The GET_BIT function is not supported in Databricks SQL. The following example
-- shows how to convert it to a Databricks equivalent
--
-- tsql sql:
SELECT GET_BIT(42, 7);

-- databricks sql:
SELECT GETBIT(42, 7);;
