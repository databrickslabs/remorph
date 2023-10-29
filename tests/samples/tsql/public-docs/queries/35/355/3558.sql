-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/object-id-transact-sql?view=sql-server-ver16

USE master;  
GO  
SELECT OBJECT_ID(N'AdventureWorks2022.Production.WorkOrder') AS 'Object ID';  
GO