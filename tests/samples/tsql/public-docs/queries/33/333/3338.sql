-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/object-name-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
SELECT DISTINCT OBJECT_NAME(object_id)  
FROM master.sys.objects;  
GO