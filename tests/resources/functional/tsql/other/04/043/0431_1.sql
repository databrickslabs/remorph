-- tsql sql:
CREATE TABLE #CustomerTable
(
    CustomerID INT,
    CustomerName VARCHAR(50),
    OrderTotal DECIMAL(10, 2)
);

WITH CustomerData AS
(
    SELECT 1 AS CustomerID, 'John' AS CustomerName, 100 AS OrderTotal
    UNION ALL
    SELECT 2 AS CustomerID, 'Jane' AS CustomerName, 200 AS OrderTotal
    UNION ALL
    SELECT 3 AS CustomerID, 'Bob' AS CustomerName, 300 AS OrderTotal
    UNION ALL
    SELECT 4 AS CustomerID, 'Alice' AS CustomerName, 400 AS OrderTotal
    UNION ALL
    SELECT 5 AS CustomerID, 'Mike' AS CustomerName, 500 AS OrderTotal
    UNION ALL
    SELECT 6 AS CustomerID, 'Emma' AS CustomerName, 600 AS OrderTotal
    UNION ALL
    SELECT 7 AS CustomerID, 'David' AS CustomerName, 700 AS OrderTotal
    UNION ALL
    SELECT 8 AS CustomerID, 'Sophia' AS CustomerName, 800 AS OrderTotal
)
INSERT INTO #CustomerTable (CustomerID, CustomerName, OrderTotal)
SELECT
    CustomerID,
    CustomerName,
    OrderTotal
FROM CustomerData;

SELECT * FROM #CustomerTable;

-- REMORPH CLEANUP: DROP TABLE #CustomerTable;
