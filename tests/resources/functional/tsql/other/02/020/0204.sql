--Query type: TCL
DECLARE @transactionSuccess BIT = 1;

BEGIN TRY
    WITH tempResult AS (
        SELECT 1 AS testValue
    )
    SELECT testValue
    FROM tempResult;

    IF @transactionSuccess = 1
        PRINT 'Transaction successful';
    ELSE
        RAISERROR ('Transaction failed', 16, 1);
END TRY

BEGIN CATCH
    PRINT 'Error occurred, rolling back transaction';
    SET @transactionSuccess = 0;
END CATCH;