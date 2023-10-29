-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/file-name-transact-sql?view=sql-server-ver16

SELECT FILE_NAME(1) AS 'File Name 1', FILE_NAME(2) AS 'File Name 2';  
GO