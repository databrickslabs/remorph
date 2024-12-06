-- tsql sql:
CREATE TABLE Orders (OrderID INT, OrderDate DATE);
INSERT INTO Orders (OrderID, OrderDate) VALUES (1, '2022-01-01');
WITH inserted AS (
    SELECT OrderID, OrderDate
    FROM Orders
    WHERE OrderID = 1
)
SELECT *
FROM inserted;
DECLARE @msg nvarchar(50) = 'Notify Order Fulfillment';
RAISERROR (@msg, 16, 10);
SELECT *
FROM Orders;
-- REMORPH CLEANUP: DROP TABLE Orders;
