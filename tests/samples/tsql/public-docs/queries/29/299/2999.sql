-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/datefirst-transact-sql?view=sql-server-ver16

SET DATEFIRST 3;
GO  
SELECT @@DATEFIRST; -- 3 (Wednesday)
GO