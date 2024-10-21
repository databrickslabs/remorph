--Query type: TCL
SET XACT_ABORT ON;

BEGIN TRY
    BEGIN TRANSACTION;

    CREATE TABLE #Sales
    (
        SalesID INT,
        Amount INT,
        Date DATE
    );

    INSERT INTO #Sales (SalesID, Amount, Date)
    VALUES
    (
        1, 100, '2022-01-01',
        2, 200, '2022-01-02',
        3, 300, '2022-01-03'
    );

    WITH Sales AS (SELECT * FROM #Sales)
    DELETE FROM Sales
    WHERE SalesID = 1;

    COMMIT TRANSACTION;

    SELECT * FROM #Sales;

END TRY

BEGIN CATCH
    IF (XACT_STATE()) = -1
    BEGIN
        PRINT 'The transaction is in an uncommittable state.' + ' Rolling back transaction.';
        ROLLBACK TRANSACTION;
    END;

    IF (XACT_STATE()) = 1
    BEGIN
        PRINT 'The transaction is committable.' + ' Committing transaction.';
        COMMIT TRANSACTION;
    END;

END CATCH;

-- REMORPH CLEANUP: DROP TABLE #Sales;