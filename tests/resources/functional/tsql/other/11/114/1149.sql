--Query type: DDL
WITH SalesData AS (
    SELECT *
    FROM (
        VALUES
            (1, 'Product1'),
            (2, 'Product2')
    ) AS Sales (ProductID, ProductName)
)
SELECT
    ProductID,
    ProductName,
    ROW_NUMBER() OVER (ORDER BY ProductID) AS RowNumber
FROM
    SalesData;

CREATE SEQUENCE Sales.CountBy1;
-- REMORPH CLEANUP: DROP SEQUENCE Sales.CountBy1;