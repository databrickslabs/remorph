--Query type: DML
DECLARE @g geometry;
SET @g = geometry::STLineFromText('LINESTRING (100 100 100 100, 200 200 200 200)', 0);
WITH GeometryCTE AS (
    SELECT @g AS geom
)
SELECT geom.ToString() AS GeometryString
FROM GeometryCTE
