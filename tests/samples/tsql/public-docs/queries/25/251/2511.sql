-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/select-group-by-transact-sql?view=sql-server-ver16

SELECT Country, Region, SUM(sales) AS TotalSales
FROM Sales
GROUP BY Country, Region;