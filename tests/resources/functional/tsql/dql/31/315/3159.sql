-- tsql sql:
WITH cte_person AS (
    SELECT 'Doe' AS LastName, 'John' AS FirstName, 1 AS BusinessEntityID
    UNION ALL
    SELECT 'Smith', 'Jane', 2
),
cte_employee AS (
    SELECT 1 AS BusinessEntityID
    UNION ALL
    SELECT 2
),
cte_salesorderheader AS (
    SELECT 1 AS SalesOrderID, 1 AS SalesPersonID
    UNION ALL
    SELECT 2, 2
),
cte_salesorderdetail AS (
    SELECT 1 AS SalesOrderID, 1 AS ProductID
    UNION ALL
    SELECT 2, 2
),
cte_product AS (
    SELECT 1 AS ProductID, 'BK-M68B-42' AS ProductNumber
    UNION ALL
    SELECT 2, 'BK-M68B-43'
)
SELECT DISTINCT p.LastName, p.FirstName
FROM cte_person p
JOIN cte_employee e ON e.BusinessEntityID = p.BusinessEntityID
WHERE p.BusinessEntityID IN (
    SELECT SalesPersonID
    FROM cte_salesorderheader
    WHERE SalesOrderID IN (
        SELECT SalesOrderID
        FROM cte_salesorderdetail
        WHERE ProductID IN (
            SELECT ProductID
            FROM cte_product
            WHERE ProductNumber = 'BK-M68B-42'
        )
    )
)
