--Query type: DML
WITH TempResult AS (
    SELECT Name, CostRate, Availability
    FROM (
        VALUES (N'Final Inventory', 15.00, 80.00),
               (N'Storage', 10.00, 90.00),
               (N'Shipping', 20.00, 70.00)
    ) AS TempResult (Name, CostRate, Availability)
)
INSERT INTO Sales.Region WITH (XLOCK) (Name, CostRate, Availability)
SELECT Name, CostRate, Availability
FROM TempResult
