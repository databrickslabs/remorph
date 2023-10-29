-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/abs-transact-sql?view=sql-server-ver16

DECLARE @i INT;  
SET @i = -2147483648;  
SELECT ABS(@i);  
GO