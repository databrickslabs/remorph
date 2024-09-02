--Query type: DQL
WITH cte1 AS (
    SELECT *
    FROM (
        VALUES (1, 'ProductModelID1', 10.0),
               (2, 'ProductModelID2', 20.0),
               (3, 'ProductModelID3', 30.0)
    ) AS cte (ProductModelID, ProductID, ListPrice)
),
cte2 AS (
    SELECT *
    FROM (
        VALUES (1, 'ProductModelID1', 10.0),
               (2, 'ProductModelID2', 20.0),
               (3, 'ProductModelID3', 30.0)
    ) AS cte (ProductModelID, ProductID, ListPrice)
)
SELECT p1.ProductModelID
FROM cte1 AS p1
GROUP BY p1.ProductModelID
HAVING MAX(p1.ListPrice) >= (
    SELECT AVG(p2.ListPrice) * 2
    FROM cte2 AS p2
    WHERE p1.ProductModelID = p2.ProductModelID
)