-- tsql sql:
DECLARE @g geography;
SET @g = geography::STGeomFromText('POLYGON((-71.093 42.358, -71.083 42.354, -71.083 42.363, -71.093 42.363, -71.093 42.358))', 4326);
SELECT @g.STArea() AS region_area
FROM (VALUES (1)) AS dummy(id);
