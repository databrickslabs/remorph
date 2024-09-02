--Query type: TCL
DECLARE @OrderError INT, @OrderDesc NVARCHAR(100);

BEGIN TRANSACTION;

SET @OrderError = @@ERROR;

IF (@OrderError <> 0)
BEGIN
    ROLLBACK TRANSACTION;
    SET @OrderDesc = N'An error has occurred while processing orders.';
    PRINT @OrderDesc; -- For demonstration, as we cannot use END CONVERSATION
END
ELSE
BEGIN
    COMMIT TRANSACTION;
    WITH DummyCTE AS (
        SELECT 1 AS DummyValue
    )
    SELECT * FROM DummyCTE;
END
-- REMORPH CLEANUP: None needed as no objects were created.