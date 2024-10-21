--Query type: DML
DECLARE @ProductInventory TABLE (ProductID INT, Quantity INT);
INSERT INTO @ProductInventory (ProductID, Quantity)
VALUES
    (1, 100),
    (2, 200),
    (3, 100);
UPDATE @ProductInventory
SET Quantity = 125
WHERE Quantity = 100;
SELECT *
FROM @ProductInventory;