-- tsql sql:
WITH extreme_point_collection AS (
    SELECT geography::Point(10, 20, 4326) AS g, 1 AS id
    UNION ALL
    SELECT geography::Point(30, 40, 4326) AS g, 2 AS id
    UNION ALL
    SELECT geography::Point(50, 60, 4326) AS g, 3 AS id
)
SELECT
    g,
    g.Lat AS Latitude,
    g.Long AS Longitude
FROM extreme_point_collection
ORDER BY id;
