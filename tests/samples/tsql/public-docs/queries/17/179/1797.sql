-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/square-transact-sql?view=sql-server-ver16

DECLARE @h FLOAT, @r FLOAT;  
SET @h = 5;  
SET @r = 1;  
SELECT PI()* SQUARE(@r)* @h AS 'Cyl Vol';