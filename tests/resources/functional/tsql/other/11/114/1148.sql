-- tsql sql:
CREATE SEQUENCE dbo.OrderCountBy10
    START WITH 10
    INCREMENT BY 10;

CREATE TABLE dbo.Orders
(
    OrderID INT DEFAULT (NEXT VALUE FOR dbo.OrderCountBy10),
    OrderName VARCHAR(100)
);

INSERT INTO dbo.Orders (OrderName)
VALUES ('Test Order');

SELECT *
FROM dbo.Orders;

-- REMORPH CLEANUP: DROP TABLE dbo.Orders;
-- REMORPH CLEANUP: DROP SEQUENCE dbo.OrderCountBy10;
