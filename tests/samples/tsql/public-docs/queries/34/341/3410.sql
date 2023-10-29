-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/error-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
UPDATE HumanResources.EmployeePayHistory  
    SET PayFrequency = 4  
    WHERE BusinessEntityID = 1;  
IF @@ERROR = 547
    BEGIN
    PRINT N'A check constraint violation occurred.';
    END
GO