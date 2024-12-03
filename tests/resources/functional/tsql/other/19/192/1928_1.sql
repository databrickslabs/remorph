--Query type: DML
WITH Customers AS (
    SELECT 1 AS CustomerID, 'John Doe' AS CustomerName
    UNION ALL
    SELECT 2, 'Jane Doe'
    UNION ALL
    SELECT 3, 'Bob Smith'
)
SELECT 'CustomerID: ' + CONVERT(VARCHAR, CustomerID) + ', CustomerName: ' + CustomerName AS CustomerInfo
FROM Customers;
