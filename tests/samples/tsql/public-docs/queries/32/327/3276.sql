-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/object-name-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
DECLARE @MyID INT;  
SET @MyID = (SELECT OBJECT_ID('AdventureWorks2022.Production.Product',  
    'U'));  
SELECT name, object_id, type_desc  
FROM sys.objects  
WHERE name = OBJECT_NAME(@MyID);  
GO