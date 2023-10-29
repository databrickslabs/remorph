-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/date-bucket-transact-sql?view=sql-server-ver16

SELECT DISTINCT DATE_BUCKET(DAY, 30, CAST([ShipDate] AS DATETIME2)) AS DateBucket
    , FIRST_VALUE([SalesOrderNumber]) OVER (
        ORDER BY DATE_BUCKET(DAY, 30, CAST([ShipDate] AS DATETIME2))
        ) AS First_Value_In_Bucket
    , LAST_VALUE([SalesOrderNumber]) OVER (
        ORDER BY DATE_BUCKET(DAY, 30, CAST([ShipDate] AS DATETIME2))
        ) AS Last_Value_In_Bucket
FROM [dbo].[FactInternetSales]
WHERE ShipDate BETWEEN '2011-01-03 00:00:00.000'
        AND '2011-02-28 00:00:00.000'
ORDER BY DateBucket;
GO