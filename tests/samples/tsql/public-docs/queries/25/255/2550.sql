-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/date-bucket-transact-sql?view=sql-server-ver16

SELECT DATE_BUCKET(WEEK, (
    SELECT TOP 1 CustomerKey
    FROM dbo.DimCustomer
    WHERE GeographyKey > 100
    ), (
    SELECT MAX(OrderDate)
    FROM dbo.FactInternetSales
));