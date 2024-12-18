-- tsql sql:
SELECT value AS region_name, COUNT(*) AS [number_of_regions]
FROM (
    VALUES ('North America,Europe,Asia'), ('Europe,Asia,Africa'), ('North America,South America')
) AS region (region_names)
CROSS APPLY STRING_SPLIT(region_names, ',')
GROUP BY value
HAVING COUNT(*) > 2
ORDER BY COUNT(*) DESC;
