-- tsql sql:
INSERT INTO SpatialData (GeomCol1)
SELECT *
FROM (
    VALUES (
        geometry::STGeomFromText('LINESTRING (200 200, 120 280, 280 280)', 0),
        geometry::STGeomFromText('POLYGON ((100 100, 250 100, 250 250, 100 250, 100 100))', 0)
    )
) AS GeomData(GeomCol1);
