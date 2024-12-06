-- tsql sql:
DECLARE @g geometry;
SET @g = (
    SELECT geom
    FROM (
        VALUES (
            geometry::STLineFromText('LINESTRING (100 100 100, 200 200 200)', 0)
        )
    ) AS temp(geom);
SELECT @g.ToString();
