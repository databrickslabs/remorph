-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/ceiling-transact-sql?view=sql-server-ver16

SELECT CEILING($123.45), CEILING($-123.45), CEILING($0.0);  
GO