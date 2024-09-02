--Query type: DQL
WITH SupplierParts (SupplierID, PartID, Quantity, EndDate, PartLevel, PartName) AS (
    SELECT s.SupplierID, p.PartID, s.Quantity, s.EndDate, 0 AS PartLevel, p.PartName
    FROM (
        VALUES (1, 1, 100, '2022-01-01'),
               (2, 2, 200, '2022-01-02')
    ) AS s (SupplierID, PartID, Quantity, EndDate)
    INNER JOIN (
        VALUES ('Part1', 1),
               ('Part2', 2)
    ) AS p (PartName, PartID) ON s.PartID = p.PartID
    WHERE s.SupplierID = 1 AND s.EndDate IS NULL
    UNION ALL
    SELECT sp.SupplierID, sp.PartID, s.Quantity, sp.EndDate, PartLevel + 1, p.PartName
    FROM (
        VALUES (1, 1, 100, '2022-01-01'),
               (2, 2, 200, '2022-01-02')
    ) AS sp (SupplierID, PartID, Quantity, EndDate)
    INNER JOIN SupplierParts AS s ON sp.PartID = s.SupplierID AND sp.EndDate IS NULL
    INNER JOIN (
        VALUES ('Part1', 1),
               ('Part2', 2)
    ) AS p (PartName, PartID) ON sp.PartID = p.PartID
)
SELECT SupplierID, PartID, PartName, Quantity, EndDate, PartLevel
FROM SupplierParts
ORDER BY PartLevel, SupplierID, PartID;