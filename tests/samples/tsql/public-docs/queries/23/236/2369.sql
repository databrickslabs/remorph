-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/sql-server-collation-name-transact-sql?view=sql-server-ver16

SELECT * FROM sys.fn_helpcollations()
WHERE name LIKE 'SQL%';