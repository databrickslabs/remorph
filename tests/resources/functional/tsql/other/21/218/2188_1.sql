--Query type: DDL
IF OBJECT_ID('[region_temp]', 'U') IS NOT NULL
    DROP TABLE [region_temp];

WITH region AS (
    SELECT 1 AS r_regionkey, 'North' AS r_name
    UNION ALL
    SELECT 2, 'South'
    UNION ALL
    SELECT 3, 'East'
    UNION ALL
    SELECT 4, 'West'
)
SELECT r_name
FROM region
WHERE r_regionkey = 1;
-- REMORPH CLEANUP: DROP TABLE [region_temp];
