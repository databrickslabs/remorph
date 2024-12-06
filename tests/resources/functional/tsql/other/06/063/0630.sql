-- tsql sql:
DECLARE @RESULT VARCHAR(100);

BEGIN TRY
    WITH TempResult AS (
        SELECT 'No error so far (but there will be).' AS RESULT
    )
    SELECT @RESULT = RESULT FROM TempResult;
    DECLARE @e1 INT = 1 / 0;
    PRINT 'Inner exception raised.';
END TRY
BEGIN CATCH
    SET @RESULT = 'Outer exception raised.';
    PRINT 'Outer exception raised.';
    PRINT ERROR_MESSAGE();
END CATCH;

PRINT @RESULT;
-- REMORPH CLEANUP: No objects created, so no cleanup needed.
