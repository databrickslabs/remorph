--Query type: DQL
WITH temp_result AS (SELECT geometry::STGeomFromText('LINESTRING(0 0, 2 2, 1 0)', 0) AS geom)
SELECT geom.STPointN(2).ToString()
FROM temp_result
