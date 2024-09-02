--Query type: DML
BEGIN TRY
    EXECUTE usp_DemoProc;
END TRY
BEGIN CATCH
    WITH ErrorCTE AS (
        SELECT ERROR_NUMBER() AS ErrorNumber,
               ERROR_MESSAGE() AS ErrorMessage
    )
    INSERT INTO ErrorLog (ErrorNumber, ErrorMessage)
    SELECT ErrorNumber, ErrorMessage FROM ErrorCTE;
END CATCH