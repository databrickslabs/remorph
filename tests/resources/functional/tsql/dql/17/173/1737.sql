-- tsql sql:
WITH temp_result AS (SELECT geometry::STGeomFromText('LINESTRING(0 0, 2 2, 0 2, 2 0)', 0) AS geom)
SELECT geom.STIsSimple() AS is_simple
FROM temp_result
