-- tsql sql:
WITH temp_result AS (SELECT 'drop_procedure' AS action)
SELECT CASE WHEN OBJECT_ID('Sales.uspDropProcedure', 'P') IS NOT NULL THEN 'DROP PROCEDURE Sales.uspDropProcedure;' ELSE '' END AS drop_statement
FROM temp_result;
-- REMORPH CLEANUP: DROP PROCEDURE Sales.uspDropProcedure;
