-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/logical-functions-greatest-transact-sql?view=azuresqldb-current

SELECT P.Name,
    P.SellStartDate,
    P.DiscontinuedDate,
    PM.ModifiedDate AS ModelModifiedDate,
    GREATEST(P.SellStartDate, P.DiscontinuedDate, PM.ModifiedDate) AS LatestDate
FROM SalesLT.Product AS P
INNER JOIN SalesLT.ProductModel AS PM
    ON P.ProductModelID = PM.ProductModelID
WHERE GREATEST(P.SellStartDate, P.DiscontinuedDate, PM.ModifiedDate) >= '2007-01-01'
    AND P.SellStartDate >= '2007-01-01'
    AND P.Name LIKE 'Touring %'
ORDER BY P.Name;