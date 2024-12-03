--Query type: DQL
WITH temp_result AS (SELECT geometry::STGeomFromText('LINESTRING(1 1, 2 2, 3 3, 4 4)', 0) AS geom)
SELECT geom.STStartPoint()
FROM temp_result
