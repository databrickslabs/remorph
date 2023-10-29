-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/object-definition-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
SELECT OBJECT_DEFINITION (OBJECT_ID(N'sys.sp_columns')) AS [Object Definition];  
GO