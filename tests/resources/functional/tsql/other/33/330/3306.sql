-- tsql sql:
CREATE TABLE dbo.CustomerOrders
(
    CustomerID NVARCHAR(11) NOT NULL,
    OrderDate DATE NOT NULL,
    TotalCost DECIMAL(10, 2) NOT NULL,
    OrderStatus NVARCHAR(20) NOT NULL
);

INSERT INTO dbo.CustomerOrders
(
    CustomerID,
    OrderDate,
    TotalCost,
    OrderStatus
)
SELECT *
FROM (
    VALUES
    (
        'C001',
        '2022-01-01',
        100.00,
        'Pending'
    ),
    (
        'C002',
        '2022-01-15',
        200.00,
        'Shipped'
    )
) AS temp_result
(
    CustomerID,
    OrderDate,
    TotalCost,
    OrderStatus
);

SELECT *
FROM dbo.CustomerOrders;
-- REMORPH CLEANUP: DROP TABLE dbo.CustomerOrders;
