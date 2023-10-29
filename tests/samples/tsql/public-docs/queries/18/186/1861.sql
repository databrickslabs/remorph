-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/execute-transact-sql?view=sql-server-ver16

DECLARE @retstat INT;  
EXECUTE @retstat = SQLSERVER1.AdventureWorks2022.dbo.uspGetEmployeeManagers @BusinessEntityID = 6;