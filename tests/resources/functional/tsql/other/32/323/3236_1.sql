--Query type: DDL
CREATE PROCEDURE #drop_procedure
AS
BEGIN
    IF EXISTS (
        SELECT 1
        FROM sys.objects
        WHERE object_id = OBJECT_ID(N'Sales.usp_UpdateOrder', N'P')
    )
    BEGIN
        DROP PROCEDURE Sales.usp_UpdateOrder;
        PRINT 'Procedure dropped.';
    END
    ELSE
    BEGIN
        PRINT 'Procedure does not exist.';
    END
END;
EXEC #drop_procedure;
-- REMORPH CLEANUP: DROP PROCEDURE #drop_procedure;