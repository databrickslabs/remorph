--Query type: DQL
WITH g1 AS (
    SELECT geography::Point(10, 10, 4326) AS geom
),
 g2 AS (
    SELECT geography::Point(20, 20, 4326) AS geom
)
SELECT g1.geom.STUnion(g2.geom) AS collected_geoms
FROM g1
CROSS JOIN g2;
