-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/error-severity-transact-sql?view=sql-server-ver16

BEGIN TRY  
    -- Generate a divide-by-zero error.  
    SELECT 1/0;  
END TRY  
BEGIN CATCH  
    SELECT ERROR_SEVERITY() AS ErrorSeverity;  
END CATCH;  
GO