-- tsql sql:
CREATE PROCEDURE usp_GetErrorInfo
AS
WITH ErrorInfo AS (
    SELECT ERROR_NUMBER() AS ErrorNumber,
           ERROR_SEVERITY() AS ErrorSeverity,
           ERROR_STATE() AS ErrorState,
           ERROR_PROCEDURE() AS ErrorProcedure,
           ERROR_LINE() AS ErrorLine,
           ERROR_MESSAGE() AS ErrorMessage
)
SELECT ErrorNumber,
       ErrorSeverity,
       ErrorState,
       ErrorProcedure,
       ErrorLine,
       ErrorMessage
FROM ErrorInfo;
