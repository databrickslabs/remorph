--Query type: DML
CREATE TABLE #ProductPriceHistory
(
    ProductID INT,
    StandardCost DECIMAL(10, 2),
    EndDate DATE
);

INSERT INTO #ProductPriceHistory (ProductID, StandardCost, EndDate)
VALUES
    (1, 10.00, NULL),
    (2, 12.50, '2022-01-01'),
    (3, 13.00, NULL),
    (4, 14.50, '2022-02-01'),
    (5, 11.00, NULL);

DELETE FROM #ProductPriceHistory
WHERE StandardCost BETWEEN 12.00 AND 14.00 AND EndDate IS NULL;

DECLARE @RowCount INT = @@ROWCOUNT;
PRINT 'Number of rows deleted is ' + CAST(@RowCount as char(3));

SELECT * FROM #ProductPriceHistory;

-- REMORPH CLEANUP: DROP TABLE #ProductPriceHistory;