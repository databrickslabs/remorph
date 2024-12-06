-- tsql sql:
DECLARE @g geometry;

SELECT @g = geom
FROM (
    SELECT geometry::STMLineFromText('MULTILINESTRING ((100 100, 200 200), (3 4, 7 8, 10 10))', 0) AS geom
) AS GeometryData;

SELECT @g.ToString() AS geom_string;
