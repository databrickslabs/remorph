-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/select-local-variable-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks2022LT
DECLARE @var1 VARCHAR(30);
SELECT @var1 = 'Generic Name';

SELECT @var1 = [Name]
FROM SalesLT.Product
WHERE ProductID = 1000000; --Value does not exist
SELECT @var1 AS 'ProductName';