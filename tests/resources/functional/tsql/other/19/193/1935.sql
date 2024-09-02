--Query type: DML
CREATE TABLE #ProductCostHistory
(
    ProductID INT,
    StandardCost DECIMAL(10, 2)
);

INSERT INTO #ProductCostHistory (ProductID, StandardCost)
VALUES
    (1, 1001.00),
    (2, 500.00),
    (3, 1200.00);

DELETE FROM #ProductCostHistory
WHERE StandardCost > 1000.00;

SELECT *
FROM #ProductCostHistory;

-- REMORPH CLEANUP: DROP TABLE #ProductCostHistory;