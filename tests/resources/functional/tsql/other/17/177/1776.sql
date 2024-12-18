-- tsql sql:
DECLARE @g geometry;
SET @g = geometry::STMPointFromText('MULTIPOINT ((100 100), (200 200))', 0);
WITH temp AS (
    SELECT @g.ToString() AS geometry_point
)
SELECT * FROM temp;
