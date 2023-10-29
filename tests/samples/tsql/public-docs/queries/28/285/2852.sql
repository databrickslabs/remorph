-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/logical-functions-iif-transact-sql?view=sql-server-ver16

SELECT [Result] = IIF( 45 > 30, NULL, NULL );