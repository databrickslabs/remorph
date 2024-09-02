--Query type: DML
CREATE PROCEDURE MyStoredProcedure
AS
BEGIN
    PRINT 'Hello, World!';
END;
GO
EXEC MyStoredProcedure;
GO
WITH MyCTE AS (
    SELECT 'Hello' AS name
)
SELECT *
FROM MyCTE;
GO
EXEC sp_bindefault 'mydefault', 'name';
GO
-- REMORPH CLEANUP: DROP PROCEDURE MyStoredProcedure;
