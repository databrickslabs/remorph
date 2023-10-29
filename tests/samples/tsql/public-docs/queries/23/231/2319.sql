-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/from-transact-sql?view=sql-server-ver16

SELECT *
FROM Sales.Customer TABLESAMPLE SYSTEM(10 PERCENT);