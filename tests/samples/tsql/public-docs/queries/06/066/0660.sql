-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-queue-transact-sql?view=sql-server-ver16

ALTER QUEUE ExpenseQueue  
    WITH ACTIVATION (  
        PROCEDURE_NAME = AdventureWorks2022.dbo.new_stored_proc ,  
        EXECUTE AS 'SecurityAccount') ;