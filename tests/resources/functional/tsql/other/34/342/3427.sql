--Query type: DML
CREATE TABLE #Product
(
    ProductID INT,
    ListPrice DECIMAL(10, 2)
);

INSERT INTO #Product (ProductID, ListPrice)
VALUES
    (1, 100.00),
    (2, 200.00),
    (3, 300.00),
    (4, 400.00),
    (5, 500.00);

DECLARE @AveragePrice DECIMAL(10, 2) = (SELECT AVG(ListPrice) FROM #Product);

WHILE @AveragePrice < 300
BEGIN
    UPDATE #Product
    SET ListPrice = ListPrice * 2;

    SET @AveragePrice = (SELECT AVG(ListPrice) FROM #Product);

    IF (SELECT MAX(ListPrice) FROM #Product) > 500
        BREAK;
    ELSE
        CONTINUE;

    PRINT 'Too much for the market to bear';
END;

SELECT * FROM #Product;
-- REMORPH CLEANUP: DROP TABLE #Product;