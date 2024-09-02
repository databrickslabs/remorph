--Query type: DML
DECLARE @g geometry;
SELECT @g = geom
FROM (
    VALUES ('LINESTRING(3 4, 8 11)')
) AS GeometrySubquery (geom);
SELECT @g.BufferWithCurves(0).ToString() AS BufferedGeometry;