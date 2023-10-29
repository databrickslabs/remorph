-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/date-bucket-transact-sql?view=sql-server-ver16

SELECT DATE_BUCKET(WEEK, 1, CAST(ShipDate AS DATETIME2)) AS ShippedDateBucket
    , SUM(OrderQuantity) AS SumOrderQuantity
    , SUM(UnitPrice) AS SumUnitPrice
FROM dbo.FactInternetSales FIS
WHERE ShipDate BETWEEN '2011-01-03 00:00:00.000'
        AND '2011-02-28 00:00:00.000'
GROUP BY DATE_BUCKET(WEEK, 1, CAST(ShipDate AS DATETIME2))
ORDER BY ShippedDateBucket;