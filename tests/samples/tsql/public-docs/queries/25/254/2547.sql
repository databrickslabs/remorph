-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/datetrunc-transact-sql?view=sql-server-ver16

SELECT DATETRUNC(m, SYSDATETIME());

SELECT DATETRUNC(yyyy, CONVERT(date, '2021-12-1'));

USE WideWorldImporters;
GO
SELECT DATETRUNC(month, DATEADD(month, 4, TransactionDate))
FROM Sales.CustomerTransactions;
GO