-- tsql sql:
DECLARE @geom geometry = geometry::STGeomFromText('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))', 0);
SET @geom = @geom.MakeValid();
SELECT IsValid, Area
FROM (VALUES (@geom.STIsValid(), @geom.STArea())) AS temp(IsValid, Area);
