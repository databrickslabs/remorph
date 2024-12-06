-- tsql sql:
DECLARE @region geometry;
SET @region = geometry::STGeomFromText('POLYGON((10 10, 20 10, 20 20, 10 20, 10 10))', 13);
SELECT *
FROM (
    VALUES (@region.STSrid)
) AS temp(region_srid);
