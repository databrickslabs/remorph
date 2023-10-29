-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/file-id-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
SELECT FILE_ID('AdventureWorks2022_Data')AS 'File ID';  
GO