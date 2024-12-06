-- tsql sql:
WITH geom1 AS (SELECT geography::Point(1, 1, 4326) AS geom),
    geom2 AS (SELECT geography::Point(2, 2, 4326) AS geom)
SELECT geom1.geom.STIntersection(geom2.geom).STAsText()
FROM geom1
CROSS JOIN geom2;
