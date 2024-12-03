--Query type: DML
CREATE TABLE #TempResult (Result INT);
INSERT INTO #TempResult
EXEC usp_GeneratedProc;
BEGIN TRY
    SELECT *
    FROM #TempResult;
END TRY
BEGIN CATCH
    SELECT ERROR_NUMBER() AS ErrorNumber,
           ERROR_SEVERITY() AS ErrorSeverity,
           ERROR_STATE() AS ErrorState,
           ERROR_PROCEDURE() AS ErrorProcedure,
           ERROR_MESSAGE() AS ErrorMessage,
           ERROR_LINE() AS ErrorLine;
END CATCH;
DROP TABLE #TempResult;
-- REMORPH CLEANUP: DROP TABLE #TempResult;
GO
