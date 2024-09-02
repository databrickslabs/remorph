--Query type: DML
DECLARE @ComparePrice DECIMAL(10, 2), @Cost DECIMAL(10, 2), @Message VARCHAR(100);

DECLARE @ProductList TABLE (
    ProductID INT,
    ProductName VARCHAR(50),
    Price DECIMAL(10, 2)
);

WITH ProductCTE AS (
    SELECT ProductID, ProductName, ListPrice
    FROM (
        VALUES (1, 'Product1', 100.00),
               (2, 'Product2', 200.00)
    ) AS Product(ProductID, ProductName, ListPrice)
    WHERE ProductName LIKE '%Product%' AND ListPrice <= 100.00
)
INSERT INTO @ProductList (ProductID, ProductName, Price)
SELECT ProductID, ProductName, ListPrice
FROM ProductCTE;

SET @Cost = (SELECT TOP 1 Price FROM @ProductList);

EXECUTE uspComparePrice @Cost, @Message OUTPUT;

IF @Cost <= 100.00
BEGIN
    PRINT 'These products can be purchased for less than $' + RTRIM(CAST(100.00 AS VARCHAR(20)));
END
ELSE
    PRINT 'The prices for all products in this category exceed $' + RTRIM(CAST(100.00 AS VARCHAR(20)));

PRINT @Message;