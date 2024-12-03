--Query type: DQL
DECLARE @g1 INT, @g2 INT;

WITH geography_data AS (
    SELECT geography::Point(10, 20, 4326) AS geo
    UNION ALL
    SELECT geography::Point(30, 40, 4326) AS geo
)

SELECT @g1 = geo.STNumPoints(), @g2 = geo.STNumPoints()
FROM geography_data;

SELECT @g1, @g2;
