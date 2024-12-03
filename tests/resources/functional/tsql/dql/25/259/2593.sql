--Query type: DQL
WITH CustomerCTE AS (
    SELECT CustomerID, NationID
    FROM (
        VALUES (1, 1), (2, 2), (3, 3)
    ) AS Customer(CustomerID, NationID)
),
RegionCTE AS (
    SELECT RegionID, NationID
    FROM (
        VALUES (1, 1), (2, 2), (3, 3)
    ) AS Region(RegionID, NationID)
)
SELECT c.CustomerID, r.RegionID
FROM CustomerCTE c
INNER JOIN RegionCTE r ON c.NationID = r.NationID;
