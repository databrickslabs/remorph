-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/fileproperty-transact-sql?view=sql-server-ver16

SELECT FILEPROPERTY('AdventureWorks2022_Data', 'IsPrimaryFile')AS [Primary File];  
GO