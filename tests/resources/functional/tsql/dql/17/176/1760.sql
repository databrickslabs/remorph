--Query type: DQL
DECLARE @region geometry;
SET @region = geometry::STGeomFromText('POLYGON((10 10, 20 10, 20 20, 10 20, 10 10),(15 15, 15 12, 12 12, 12 15, 15 15))', 0);
SELECT geom.STArea() AS region_area
FROM (VALUES (@region)) AS region(geom);
