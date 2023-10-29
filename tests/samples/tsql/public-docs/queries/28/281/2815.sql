-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/charindex-transact-sql?view=sql-server-ver16

SELECT TOP(1) CHARINDEX('at', 'This is a string') FROM dbo.DimCustomer;