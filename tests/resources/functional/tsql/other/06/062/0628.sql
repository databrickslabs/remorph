--Query type: DML
DECLARE @my_exception INT;

BEGIN TRY
    RAISERROR ('Test Error', 16, 1);
END TRY

BEGIN CATCH
    IF ERROR_NUMBER() = 1205
        SELECT 'Error type' = 'STATEMENT_ERROR',
               'SQLCODE' = ERROR_NUMBER(),
               'SQLERRM' = ERROR_MESSAGE(),
               'SQLSTATE' = ERROR_STATE();
    ELSE IF ERROR_NUMBER() = 3621
        SELECT 'Error type' = 'EXPRESSION_ERROR',
               'SQLCODE' = ERROR_NUMBER(),
               'SQLERRM' = ERROR_MESSAGE(),
               'SQLSTATE' = ERROR_STATE();
    ELSE
        SELECT 'Error type' = 'Other error',
               'SQLCODE' = ERROR_NUMBER(),
               'SQLERRM' = ERROR_MESSAGE(),
               'SQLSTATE' = ERROR_STATE();
END CATCH;
