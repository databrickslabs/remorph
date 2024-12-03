--Query type: DML
WITH DataToInsert AS (
    SELECT 'Damaged Goods' AS Name, 5 AS CostRate, 2.5 AS Availability, GETDATE() AS ModifiedDate
    UNION ALL
    SELECT 'New Goods', 10, 5.0, GETDATE()
    UNION ALL
    SELECT 'Used Goods', 2, 1.5, GETDATE()
)
INSERT INTO #Location (Name, CostRate, Availability, ModifiedDate)
SELECT Name, CostRate, Availability, ModifiedDate
FROM DataToInsert;
