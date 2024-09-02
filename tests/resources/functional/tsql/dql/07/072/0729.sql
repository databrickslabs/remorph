--Query type: DQL
WITH temp_table AS (
    SELECT 1 AS point_id, geography::Point(42.3152, -71.0882, 4326) AS point_c, geography::Point(42.3202, -71.0934, 4326) AS point_d
)
SELECT LEFT(point_c.STAsText(), 9) AS geohash_of_point_c, LEFT(point_d.STAsText(), 9) AS geohash_of_point_d
FROM temp_table;