-- tsql sql:
DECLARE @g geometry;
WITH g AS (
    SELECT geometry::Parse('CURVEPOLYGON EMPTY') AS geom
)
SELECT geom.STCurveToLine() AS CurveToLineType, geom.STGeometryType() AS CurveType
FROM g;
SET @g = geometry::Parse('LINESTRING EMPTY');
SELECT @g.STGeometryType() AS LineType;
