-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/left-transact-sql?view=sql-server-ver16

SELECT LEFT(Name, 5)   
FROM Production.Product  
ORDER BY ProductID;  
GO