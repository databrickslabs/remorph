--Query type: DML
CREATE PROCEDURE uspGetProductDetails
    @ProductID INT
AS
BEGIN
    WITH ProductCTE AS (
        SELECT ProductID, ProductName, ProductNumber, ListPrice
        FROM (
            VALUES (1, 'Product A', 'PA-001', 100.00),
                   (2, 'Product B', 'PB-002', 200.00),
                   (3, 'Product C', 'PC-003', 300.00)
        ) p (ProductID, ProductName, ProductNumber, ListPrice)
    )
    SELECT p.ProductID, p.ProductName, p.ProductNumber, p.ListPrice
    FROM ProductCTE p
    WHERE p.ProductID = @ProductID
      AND p.ListPrice > (
            SELECT AVG(ListPrice)
            FROM (
                VALUES (100.00),
                       (200.00),
                       (300.00)
            ) lp (ListPrice)
        );
END;

DECLARE @ProductIDForExecution INT;
SET @ProductIDForExecution = 1;
EXEC uspGetProductDetails @ProductIDForExecution;

WITH ProductCTE AS (
    SELECT ProductID, ProductName, ProductNumber, ListPrice
    FROM (
        VALUES (1, 'Product A', 'PA-001', 100.00),
               (2, 'Product B', 'PB-002', 200.00),
               (3, 'Product C', 'PC-003', 300.00)
    ) p (ProductID, ProductName, ProductNumber, ListPrice)
)
SELECT p.ProductID, p.ProductName, p.ProductNumber, p.ListPrice
FROM ProductCTE p;

-- REMORPH CLEANUP: DROP PROCEDURE uspGetProductDetails;