-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/file-idex-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
SELECT FILE_IDEX((SELECT TOP (1) name FROM sys.database_files WHERE type = 1)) AS 'File ID';  
GO