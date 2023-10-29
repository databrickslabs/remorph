-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/file-idex-transact-sql?view=sql-server-ver16

SELECT FILE_IDEX((SELECT name FROM sys.master_files WHERE type = 4))  
AS 'File_ID';