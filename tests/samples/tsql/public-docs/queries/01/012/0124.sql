-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/set-arithignore-transact-sql?view=sql-server-ver16

-- SET ARITHIGNORE OFF and testing.  
SET ARITHIGNORE OFF;  
SELECT 1 / 0 AS DivideByZero;  
SELECT CAST(256 AS TINYINT) AS Overflow;