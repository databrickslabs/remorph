-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/last-value-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO
SELECT BusinessEntityID
    , DATEPART(QUARTER, QuotaDate) AS Quarter
    , YEAR(QuotaDate) AS SalesYear
    , SalesQuota AS QuotaThisQuarter
    , SalesQuota - FIRST_VALUE(SalesQuota)
          OVER (PARTITION BY BusinessEntityID, YEAR(QuotaDate)
              ORDER BY DATEPART(QUARTER, QuotaDate)) AS DifferenceFromFirstQuarter
    , SalesQuota - LAST_VALUE(SalesQuota)
          OVER (PARTITION BY BusinessEntityID, YEAR(QuotaDate)
              ORDER BY DATEPART(QUARTER, QuotaDate)
              RANGE BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING) AS DifferenceFromLastQuarter
FROM Sales.SalesPersonQuotaHistory
WHERE YEAR(QuotaDate) > 2005 AND BusinessEntityID BETWEEN 274 AND 275
ORDER BY BusinessEntityID, SalesYear, Quarter;