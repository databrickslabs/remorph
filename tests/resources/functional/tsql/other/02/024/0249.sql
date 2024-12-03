--Query type: DML
CREATE PROCEDURE my_stored_procedure @limit INT AS BEGIN SELECT 'Spending limit set to ' + CONVERT(VARCHAR, @limit) AS message; END; EXEC my_stored_procedure 500; -- REMORPH CLEANUP: DROP PROCEDURE my_stored_procedure;
