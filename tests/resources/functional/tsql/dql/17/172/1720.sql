-- tsql sql:
DECLARE @geom geometry;
SET @geom = geometry::STGeomFromText('CURVEPOLYGON(CIRCULARSTRING(0 0, 2 2, 0 2, -2 2, 0 0))', 0);
SELECT @geom.STBoundary().ToString();
