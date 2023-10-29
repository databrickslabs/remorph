-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/windows-collation-name-transact-sql?view=sql-server-ver16

SELECT * FROM sys.fn_helpcollations() WHERE [name] NOT LIKE N'SQL%';