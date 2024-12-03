--Query type: DQL
WITH cte (SupplierID, NationID, RegionID) AS (
    SELECT SupplierID, NationID, RegionID
    FROM (
        VALUES (1, 1, 1),
               (2, 2, 2),
               (3, 3, 3)
    ) AS Supplier(SupplierID, NationID, RegionID)
    WHERE NationID IS NOT NULL
)
SELECT cte.SupplierID, cte.NationID, cte.RegionID
FROM cte
CROSS JOIN (
    VALUES (1, 1),
           (2, 2),
           (3, 3)
) AS Nation(NationID, RegionID)
WHERE cte.NationID = Nation.NationID;
