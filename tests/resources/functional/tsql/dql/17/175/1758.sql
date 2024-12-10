-- tsql sql:
DECLARE @customer geometry;
SET @customer = geometry::STGeomFromText('POLYGON((0 0, 3 0, 3 3, 0 3, 0 0))', 0);
WITH customer AS (
    SELECT @customer AS geom
)
SELECT geom.STGeometryType()
FROM customer
