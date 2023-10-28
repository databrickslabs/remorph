SELECT Country, Region, SUM(sales) AS TotalSales
FROM Sales
GROUP BY Country, Region;