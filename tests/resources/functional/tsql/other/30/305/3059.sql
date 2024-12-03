--Query type: DML
WITH RegionsCTE AS (
    SELECT 'North' AS Name, '10.1:40.1' AS Location
    UNION ALL
    SELECT 'South', '74.0060:40.7128'
    UNION ALL
    SELECT 'East', '118.2437:34.0522'
),
UpdatedRegions AS (
    SELECT Name, CASE WHEN Name = 'North' THEN '12.3:46.2' ELSE Location END AS Location
    FROM RegionsCTE
)
SELECT *
FROM UpdatedRegions;
