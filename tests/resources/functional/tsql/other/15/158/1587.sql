-- tsql sql:
DECLARE @region_name VARCHAR(100);
SET @region_name = 'MIDDLE EAST';

WITH region AS (
    SELECT 'MIDDLE EAST' AS region_name, 1 AS region_key
    UNION ALL
    SELECT 'EUROPE', 2
    UNION ALL
    SELECT 'AFRICA', 3
)

SELECT *
FROM region
WHERE region_name = @region_name
