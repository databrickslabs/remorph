-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/logical-functions-least-transact-sql?view=azuresqldb-current

SELECT P.Name,
    P.SellStartDate,
    P.DiscontinuedDate,
    PM.ModifiedDate AS ModelModifiedDate,
    LEAST(P.SellStartDate, P.DiscontinuedDate, PM.ModifiedDate) AS EarliestDate
FROM SalesLT.Product AS P
INNER JOIN SalesLT.ProductModel AS PM
    ON P.ProductModelID = PM.ProductModelID
WHERE LEAST(P.SellStartDate, P.DiscontinuedDate, PM.ModifiedDate) >= '2007-01-01'
    AND P.SellStartDate >= '2007-01-01'
    AND P.Name LIKE 'Touring %'
ORDER BY P.Name;