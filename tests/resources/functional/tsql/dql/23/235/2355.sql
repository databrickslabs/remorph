-- tsql sql:
WITH SalesData AS (
    SELECT 1 AS StoreID, 'Store1' AS StoreName
    UNION ALL
    SELECT 2 AS StoreID, 'Store2' AS StoreName
)
SELECT *
FROM SalesData
WHERE StoreID = dbo.ufn_GetStoreID(602);
