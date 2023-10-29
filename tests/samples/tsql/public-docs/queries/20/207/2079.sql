-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/applock-test-transact-sql?view=sql-server-ver16

EXEC sp_releaseapplock @Resource='Form1', @DbPrincipal='public';  
GO