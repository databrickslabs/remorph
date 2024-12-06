-- tsql sql:
DECLARE @region_name nvarchar(50);
SET @region_name = 'Europe';

WITH regions AS (
    SELECT 'Europe' AS region_name, 1 AS region_id
    UNION ALL
    SELECT 'Asia', 2
    UNION ALL
    SELECT 'Africa', 3
)

SELECT region_id
FROM regions
WHERE region_name = @region_name;
