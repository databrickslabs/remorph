-- tsql sql:
DECLARE @geom geometry;
SET @geom = geometry::Parse('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))');
WITH temp_result AS (
    SELECT @geom.CurveToLineWithTolerance(0.1, 0).ToString() AS geom_str
)
SELECT geom_str
FROM temp_result;
