-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/procid-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
IF OBJECT_ID ( 'usp_FindName', 'P' ) IS NOT NULL   
DROP PROCEDURE usp_FindName;  
GO  
CREATE PROCEDURE usp_FindName  
    @lastname VARCHAR(40) = '%',   
    @firstname VARCHAR(20) = '%'  
AS  
DECLARE @Count INT;  
DECLARE @ProcName NVARCHAR(128);  
SELECT LastName, FirstName  
FROM Person.Person   
WHERE FirstName LIKE @firstname AND LastName LIKE @lastname;  
SET @Count = @@ROWCOUNT;  
SET @ProcName = OBJECT_NAME(@@PROCID);  
RAISERROR ('Stored procedure %s returned %d rows.', 16,10, @ProcName, @Count);  
GO  
EXECUTE dbo.usp_FindName 'P%', 'A%';