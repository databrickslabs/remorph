--Query type: DML
WITH g AS (SELECT geography::STGeomFromText('LINESTRING(0 2, 1 1, 1 0, 1 1, 2 2)', 4326) AS geom)
SELECT geom.STIsValid()
FROM g