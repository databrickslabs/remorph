-- tsql sql:
WITH cte AS (
    SELECT geography::STGeomFromText('LINESTRING(0 0, 1 1)', 4326) AS g1,
           geography::STGeomFromText('LINESTRING(1 1, 2 2)', 4326) AS g2
    UNION ALL
    SELECT geography::STGeomFromText('LINESTRING(2 2, 3 3)', 4326),
           geography::STGeomFromText('LINESTRING(3 3, 4 4)', 4326)
)
SELECT g1.STUnion(g2) AS collected_g1
FROM cte
